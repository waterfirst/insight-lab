"""SP37 measurement extraction. Reproduces every number in the article from the four public
YouTube copies (not redistributed here). Usage: python extract.py <dir with the 4 mp4s>"""
import sys, os, json, hashlib, subprocess, wave, io
import numpy as np

SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/yuk_footage")
OUT = os.path.dirname(os.path.abspath(__file__))
IDS = ["JABHMSoi1bU", "F-bDTTL8r2M", "O65Kl05hB84", "EwkcM0MYYyY"]
Q = {"JABHMSoi1bU": "Q1", "F-bDTTL8r2M": "Q2", "O65Kl05hB84": "Q3", "EwkcM0MYYyY": "Q4"}

def run(cmd):
    return subprocess.run(cmd, capture_output=True, check=True).stdout

def audio(id_, sr, ss=None, t=None):
    cmd = ["ffmpeg", "-v", "error"]
    if ss is not None: cmd += ["-ss", str(ss)]
    cmd += ["-i", f"{SRC}/{id_}.mp4"]
    if t is not None: cmd += ["-t", str(t)]
    cmd += ["-ac", "1", "-ar", str(sr), "-f", "s16le", "-"]
    return np.frombuffer(run(cmd), np.int16).astype(float) / 32768

def dump(name, obj):
    with open(f"{OUT}/{name}", "w") as f: json.dump(obj, f, ensure_ascii=False, indent=1)

# 1. evidence register
ev = []
for i in IDS:
    p = f"{SRC}/{i}.mp4"
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    pr = json.loads(run(["ffprobe", "-v", "error", "-show_entries",
        "stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate:format=duration", "-of", "json", p]))
    ev.append({"id": Q[i], "youtube_id": i, "sha256": h, "bytes": os.path.getsize(p), "probe": pr})
dump("evidence.json", ev)

# 2. lineage: log-RMS envelope (10 ms) cross-correlation, Q1 5-20 s as query
def env(x, sr, hop=0.01):
    h = int(sr * hop); n = len(x) // h
    return np.log(np.sqrt((x[:n*h].reshape(n, h) ** 2).mean(1)) + 1e-6)
ref = env(audio(IDS[0], 16000, t=60), 16000)
q = ref[500:2000]; q = (q - q.mean()) / q.std()
lin = []
for i in IDS[1:]:
    e = env(audio(i, 16000, t=60), 16000); best = (-1, 0)
    for lag in range(len(e) - len(q)):
        w = e[lag:lag+len(q)]; s = w.std()
        if s == 0: continue
        c = float(np.dot(q, (w - w.mean()) / s) / len(q))
        if c > best[0]: best = (c, lag)
    lin.append({"id": Q[i], "corr": round(best[0], 3), "offset_s": round(best[1]*0.01 - 5.0, 2)})
dump("lineage.json", lin)

# 3. bandwidth: long-term spectrum relative to 300-1000 Hz median
bw = {}
for i in IDS:
    x = audio(i, 48000, t=60); N = 8192; S = np.zeros(N//2+1); c = 0
    for k in range(0, len(x)-N, N//2):
        S += np.abs(np.fft.rfft(x[k:k+N]*np.hanning(N)))**2; c += 1
    f = np.fft.rfftfreq(N, 1/48000); db = 10*np.log10(S/c + 1e-20)
    ref_ = np.median(db[(f > 300) & (f < 1000)])
    cen = np.arange(125, 20000, 250)
    bw[Q[i]] = [round(float(np.median(db[(f >= a-125) & (f < a+125)]) - ref_), 1) for a in cen]
bw["freq_hz"] = [int(a) for a in np.arange(125, 20000, 250)]
dump("bandwidth.json", bw)

# 4. ROI motion (Q1, 0-20 s, 30 fps grayscale)
W, H = 640, 480
F = np.frombuffer(run(["ffmpeg", "-v", "error", "-i", f"{SRC}/{IDS[0]}.mp4", "-t", "20",
    "-f", "rawvideo", "-pix_fmt", "gray", "-"]), np.uint8).reshape(-1, H, W).astype(np.float32)
ROI = {"podium_speaker": (265, 300, 95, 140), "stage_person_A": (280, 355, 220, 300),
       "hanbok_seat": (305, 355, 380, 425)}
t = np.arange(1, len(F)) / 30
mot = {"t": [round(v, 4) for v in t],
       "global": [round(float(v), 3) for v in np.abs(np.diff(F, axis=0)).mean(axis=(1, 2))]}
first = {}
for k, (y0, y1, x0, x1) in ROI.items():
    d = np.abs(np.diff(F[:, y0:y1, x0:x1], axis=0)).mean(axis=(1, 2)); mot[k] = [round(float(v), 3) for v in d]
    base = d[int(5*30):int(9.5*30)]; thr = np.median(base) + 5*np.std(base)
    idx = np.where((t > 9.5) & (d > thr))[0]; first[k] = round(float(t[idx[0]]), 3) if len(idx) else None
mot["roi_yx"] = {k: list(v) for k, v in ROI.items()}; mot["first_anomaly_s"] = first
dup = int((np.abs(np.diff(F[330:402, 250:360, 200:320], axis=0)).mean(axis=(1, 2)) < 0.8).sum())
mot["duplicate_frames_11_to_13_4s"] = dup
dump("roi_motion.json", mot)

# 5. loudness + spectral flatness (20 ms) for Q1 0-20 s
x = audio(IDS[0], 16000, t=20); h = 320; n = len(x)//h; ld = []; fl = []
for k in range(n):
    s = x[k*h:(k+1)*h]*np.hanning(h); P = np.abs(np.fft.rfft(s))**2 + 1e-12; P = P[5:]
    ld.append(round(float(10*np.log10(np.mean(s**2)+1e-12)), 2)); fl.append(round(float(np.exp(np.mean(np.log(P)))/np.mean(P)), 4))
dump("loudness_flatness.json", {"t": [round(k*0.02, 2) for k in range(n)], "db": ld, "flatness": fl})

# 6. waveform zoom 9.7-10.7 s (8 kHz) and impulse rise-time test
z = audio(IDS[0], 8000, ss=9.7, t=1.0)
dump("waveform_9p7_10p7.json", {"sr": 8000, "t0": 9.7, "x": [round(float(v), 4) for v in z]})
x48 = audio(IDS[0], 48000, ss=4, t=10)
def rise(a, b, t0=4, sr=48000):
    s = x48[int((a-t0)*sr):int((b-t0)*sr)]; e = np.abs(s); i = int(np.argmax(e)); pk = e[i]
    hh = int(sr*0.0005); m = np.array([e[k*hh:(k+1)*hh].max() for k in range(len(e)//hh)])
    k = i//hh; pre = m[max(0, k-60):k+1]; r = np.where(pre < 0.1*pk)[0]; st = r[-1] if len(r) else 0
    return {"window": [a, b], "peak_t": round(a+i/sr, 4), "peak_amp": round(float(pk), 3),
            "rise_10_90_ms": round((len(pre)-1-st)*0.5, 1)}
imp = [rise(a, b) for a, b in [(4.8, 4.95), (5.95, 6.10), (7.0, 7.15), (7.9, 8.0), (9.95, 10.0), (11.1, 11.2)]]
dump("impulse_candidates.json", {"criterion_gunshot_rise_ms": 2.0, "candidates": imp})

# 7. howling: precise pitch tracks
xh = audio(IDS[0], 48000, ss=8, t=8); N = 8192; win = np.hanning(N)
def track(a, b, lo, hi, t0=8, sr=48000):
    out = []
    for s in np.arange(int((a-t0)*sr), int((b-t0)*sr)-N, 480):
        X = np.abs(np.fft.rfft(xh[s:s+N]*win)); f = np.fft.rfftfreq(N, 1/sr)
        m = (f > lo) & (f < hi); k = np.where(m)[0][np.argmax(X[m])]
        a1, b1, c1 = np.log(X[k-1:k+2]+1e-12); d = 0.5*(a1-c1)/(a1-2*b1+c1); f0 = (k+d)*sr/N
        A = 20*np.log10(X[k]+1e-12)
        hr = [20*np.log10(X[int(round(nn*f0*N/sr))-2:int(round(nn*f0*N/sr))+3].max()+1e-12)-A for nn in (2, 3)]
        out.append([round(t0+(s+N/2)/sr, 3), round(float(f0), 2), round(float(A), 2), round(hr[0], 1), round(hr[1], 1)])
    r = np.array(out); f = r[:, 1]
    return {"band": [lo, hi], "window": [a, b], "track": out,
            "mean_hz": round(float(f.mean()), 1), "total_drift_pct": round(float((f.max()-f.min())/f.mean()*100), 2),
            "jitter_pct": round(float(np.std(np.diff(f))/f.mean()*100), 3),
            "amp_slope_db_per_s": round(float(np.polyfit(r[:, 0], r[:, 2], 1)[0]), 1),
            "h2_db": round(float(np.median(r[:, 3])), 1), "h3_db": round(float(np.median(r[:, 4])), 1)}
dump("howling.json", {"line_412": track(11.0, 11.45, 350, 500), "line_830": track(11.4, 11.8, 750, 950),
                      "voice_control": track(9.85, 10.4, 200, 400)})

# 8. ENF (mains hum) track 0-20 s around 120 Hz
xe = audio(IDS[0], 8000, t=20); sr = 8000
Xa = np.abs(np.fft.rfft(xe*np.hanning(len(xe)))); fa = np.fft.rfftfreq(len(xe), 1/sr)
lines = {}
for hz in (60, 120, 180, 240, 300):
    m = (fa > hz-3) & (fa < hz+3); nb = (fa > hz-15) & (fa < hz+15); k = int(np.argmax(Xa[m]))
    lines[hz] = {"peak_hz": round(float(fa[m][k]), 3), "prominence_db": round(float(20*np.log10(Xa[m][k]/np.median(Xa[nb]))), 1)}
Nn = sr*2; T = []; Fq = []; Pw = []
for s in range(0, len(xe)-Nn, sr//10):
    Z = np.fft.rfft(xe[s:s+Nn]*np.hanning(Nn), 8*Nn); ff = np.fft.rfftfreq(8*Nn, 1/sr)
    m = (ff > 118.5) & (ff < 121.5); k = int(np.argmax(np.abs(Z[m])))
    T.append(round((s+Nn/2)/sr, 2)); Fq.append(round(float(ff[m][k]), 3)); Pw.append(round(float(20*np.log10(np.abs(Z[m][k])+1e-9)), 2))
dump("enf.json", {"hum_lines": lines, "t": T, "f120": Fq, "power_db": Pw, "window_s": 2.0})
print("done", OUT)
