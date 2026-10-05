"""SP37 figures from the JSON data in this folder. python make_figures.py"""
import json, os, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Patch
for p in fm.findSystemFonts():
    if "NanumSquare" in p or "NotoSansCJK" in p: fm.fontManager.addfont(p)
plt.rcParams.update({"font.family": ["Noto Sans CJK KR", "NanumSquare", "DejaVu Sans"], "axes.unicode_minus": False, "figure.dpi": 130})
BLUE, GREEN, RED, GOLD, MUTED, PURP = "#38bdf8", "#22c55e", "#ef4444", "#f59e0b", "#64748b", "#a855f7"
H = os.path.dirname(os.path.abspath(__file__)); J = lambda n: json.load(open(f"{H}/{n}"))
def finish(ax, title, sub=""):
    ax.set_title(title + ("\n" + sub if sub else ""), fontsize=12, fontweight="bold", loc="left", pad=12)
    ax.spines[["top", "right"]].set_visible(False)
def save(fig, n): fig.tight_layout(); fig.savefig(f"{H}/{n}", dpi=130); plt.close(fig)
EV = {"인물 A 첫 반응": (10.6, GOLD), "연설자 은신": (12.4, RED), "한복 인물 기울어짐": (13.5, PURP)}

# fig1 lineage
lin = J("lineage.json"); fig, ax = plt.subplots(figsize=(8, 3.6))
ax.barh([d["id"] for d in lin], [d["corr"] for d in lin], color=BLUE)
for i, d in enumerate(lin): ax.text(d["corr"] + .01, i, f'r={d["corr"]:.3f}, Q1 대비 {d["offset_s"]:+.2f}s', va="center", fontsize=9)
ax.set_xlim(0, 1.25); ax.set_xlabel("Q1 음량 포락선과의 상관계수 (10ms, Q1 5–20s 기준)")
finish(ax, "그림 1. 공개 사본 4점은 하나의 음향 계통이다", "독립 증거 4개가 아니라 사실상 1개"); save(fig, "fig1_lineage.png")

# fig2 bandwidth
bw = J("bandwidth.json"); f = np.array(bw["freq_hz"]) / 1000; fig, ax = plt.subplots(figsize=(8, 3.8))
for q, c in zip(["Q1", "Q2", "Q3", "Q4"], [BLUE, GREEN, GOLD, MUTED]): ax.plot(f, bw[q], color=c, lw=1.5, label=q)
ax.axhline(-40, color=RED, ls="--", lw=.8); ax.text(15, -38, "-40dB", color=RED, fontsize=8)
ax.set_xlim(0, 16); ax.set_ylim(-80, 5); ax.set_xlabel("주파수 (kHz)"); ax.set_ylabel("300–1000Hz 대비 (dB)"); ax.legend(fontsize=8)
finish(ax, "그림 2. 고역이 깎인 음원 — 총성의 날카로운 성분이 약해진다", "Q1–Q3은 약 5.5–7kHz에서 -40dB, Q4(화면 재촬영)는 10.5kHz"); save(fig, "fig2_bandwidth.png")

# fig3 timeline
m = J("roi_motion.json"); lf = J("loudness_flatness.json"); t = np.array(m["t"])
fig, ax = plt.subplots(3, 1, figsize=(9, 7.5), sharex=True)
for k, lab, c in [("stage_person_A", "무대 위 인물 A", GOLD), ("podium_speaker", "연단(연설자)", RED), ("hanbok_seat", "한복 인물 좌석", PURP)]:
    ax[0].plot(t, m[k], color=c, lw=1, label=lab)
ax[0].plot(t, m["global"], color="k", lw=.7, label="전체 화면(카메라 대조)"); ax[0].set_ylabel("프레임 차"); ax[0].legend(fontsize=7, ncol=2)
ax[1].plot(lf["t"], lf["db"], color=BLUE, lw=.8); ax[1].set_ylabel("음량 dB")
ax[2].plot(lf["t"], lf["flatness"], color=GREEN, lw=.8); ax[2].set_ylabel("스펙트럼 평탄도"); ax[2].set_xlabel("Q1 시각 (s)")
for a in ax:
    for lab, (v, c) in EV.items(): a.axvline(v, color=c, ls="--", lw=.8)
ax[0].set_xlim(8, 16)
finish(ax[0], "그림 3. 화면 움직임과 소리를 한 시간축에", "ROI 첫 이상(5σ): 인물 A 9.93s · 연설자 12.23s · 한복 좌석 10.67s(소폭)/13.0s~(대폭)"); save(fig, "fig3_timeline.png")

# fig4 waveform
w = J("waveform_9p7_10p7.json"); x = np.array(w["x"]); tt = w["t0"] + np.arange(len(x)) / w["sr"]
fig, ax = plt.subplots(2, 1, figsize=(9, 4.6))
ax[0].plot(tt, x, lw=.4, color=BLUE); ax[0].set_xlim(9.7, 10.7); ax[0].set_ylabel("진폭")
mz = (tt > 9.90) & (tt < 9.96); ax[1].plot(tt[mz] * 1000 - 9900, x[mz], lw=.8, color=BLUE); ax[1].set_xlabel("9.900s 이후 ms"); ax[1].set_ylabel("진폭")
finish(ax[0], "그림 4. 처음 총성 후보로 본 9.85–10.4s — 실제로는 목소리", "아래 확대: 3–4ms 간격의 규칙적 성문 펄스(배음 구조). 이 판정으로 첫 후보를 철회했다"); save(fig, "fig4_waveform.png")

# fig5 impulse rise times
im = J("impulse_candidates.json")["candidates"]; fig, ax = plt.subplots(figsize=(8, 3.6))
lab = [f'{c["peak_t"]:.2f}s' for c in im]; r = [c["rise_10_90_ms"] for c in im]
ax.bar(lab, r, color=[GOLD if v < 3 else MUTED for v in r]); ax.axhline(2, color=RED, ls="--"); ax.text(len(r) - .6, 2.6, "총성 기준 2ms", color=RED, fontsize=8, ha="right")
ax.set_ylabel("상승시간 10→90% (ms)"); ax.set_xlabel("후보 피크 시각 (Q1)")
finish(ax, "그림 5. 급상승 후보 6개 중 총성 기준(<2ms)을 넘는 것은 없다", "7.93s(노랑)만 2.5ms로 근접 — 감쇠 148ms·중심 735Hz로 미판정(U1)"); save(fig, "fig5_rise.png")

# fig6 howling
hw = J("howling.json"); fig, ax = plt.subplots(1, 2, figsize=(10, 3.8), gridspec_kw={"width_ratios": [1.6, 1]})
for k, c, lab in [("line_412", RED, "412Hz 선 (11.0–11.45s)"), ("voice_control", BLUE, "목소리 대조 (9.85–10.4s)"), ("line_830", GOLD, "830Hz (11.4–11.8s)")]:
    tr = np.array(hw[k]["track"]); ax[0].plot(tr[:, 0], tr[:, 1], color=c, lw=1.3, label=lab)
ax[0].set_ylabel("추적 주파수 Hz"); ax[0].set_xlabel("Q1 시각 (s)"); ax[0].legend(fontsize=7)
names = ["412Hz", "830Hz", "목소리"]; ks = ["line_412", "line_830", "voice_control"]
ax[1].bar(names, [hw[k]["jitter_pct"] for k in ks], color=[RED, GOLD, BLUE]); ax[1].set_yscale("log"); ax[1].set_ylabel("프레임 간 떨림 % (로그)")
for i, k in enumerate(ks): ax[1].text(i, hw[k]["jitter_pct"] * 1.2, f'{hw[k]["jitter_pct"]}%\n{hw[k]["amp_slope_db_per_s"]:+.0f}dB/s', ha="center", fontsize=7)
finish(ax[0], "그림 6. 하울링 후보 — 고정된 순음이 지수적으로 커진다", "412Hz: 떨림 0.089%, 2배음 -17.6dB, +38.7dB/s"); ax[1].spines[["top", "right"]].set_visible(False); save(fig, "fig6_howling.png")

# fig7 ENF
e = J("enf.json"); fig, ax = plt.subplots(2, 1, figsize=(9, 4.6), sharex=True)
ax[0].plot(e["t"], e["f120"], color=GREEN); ax[0].set_ylabel("험 주파수 Hz"); ax[1].plot(e["t"], e["power_db"], color=MUTED); ax[1].set_ylabel("험 세기 dB"); ax[1].set_xlabel("Q1 시각 (s)")
ax[0].axvspan(12.05, 12.85, color=RED, alpha=.12); ax[0].text(12.9, 121.2, "함성 마스킹", color=RED, fontsize=8)
for a in ax:
    for lab, (v, c) in EV.items(): a.axvline(v, color=c, ls="--", lw=.7)
finish(ax[0], "그림 7. 전원 험(ENF) — 60Hz 계통, 사건 구간에서 끊기지 않는다", f'기본 {e["hum_lines"]["60"]["peak_hz"]}Hz(-0.08%) → 재생 속도 정확, 이어붙이기 흔적 미검출'); save(fig, "fig7_enf.png")

# fig8 Bae physics
v = np.linspace(200, 300, 101); fig, ax = plt.subplots(figsize=(8, 3.8))
for d, c in [(15.0, BLUE), (18.2, RED)]:
    ax.plot(v, d / v * 1000, color=c, lw=1.5, label=f"{d}m 탄환 비행시간")
    ax.plot(v, d * (1 / v - 1 / 340) * 1000, color=c, lw=1.5, ls="--", label=f"{d}m 총성 도달 후 탄환 지연")
ax.axhline(20, color=GOLD, lw=1); ax.text(201, 22, "배명진 '0.02초'", color=GOLD, fontsize=8)
ax.set_xlabel(".38 Special 탄속 가정 (m/s)"); ax.set_ylabel("ms"); ax.legend(fontsize=7)
finish(ax, "그림 8. 배명진(2005) 계산 검산", "0.02초는 비행시간(60–91ms)이 아니라 '소리 뒤 탄환 지연'으로만 근사 성립, 탄속에 민감"); save(fig, "fig8_bae_physics.png")

# fig9 timing conflict & concordance
mr = J("manual_records.json"); fig, ax = plt.subplots(figsize=(9, 3.8))
rows = mr["concordance"]
for i, r in enumerate(rows):
    ax.plot(r["claude"], [i + .12] * 2, color=BLUE, lw=6, solid_capstyle="butt"); ax.plot(r["codex"], [i - .12] * 2, "o", color=GOLD if "오측정" not in r["verdict"] else RED, ms=7)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r["event"] for r in rows], fontsize=8)
ax.plot([], [], color=BLUE, lw=6, label="Claude"); ax.plot([], [], "o", color=GOLD, label="Codex(블라인드)"); ax.plot([], [], "o", color=RED, label="Codex 오측정")
ax.set_xlim(9, 15); ax.set_xlabel("Q1 시각 (s)"); ax.legend(fontsize=7, loc="lower right")
finish(ax, "그림 9. 두 검사자의 독립 측정", "연설자 은신만 어긋났고, 원본 프레임 대조로 Codex 쪽 ROI 오류 판정"); save(fig, "fig9_concordance.png")

# fig10 ACH
a = mr["ach_v2"]; code = {"N": 0, "?": 0, "C": 2, "wC": 1, "wI": -1, "I": -2}
M = np.array([[code[c] for c in row] for row in a["codes"]], float)
fig, ax = plt.subplots(figsize=(10, 4.2)); ax.imshow(M, cmap="RdYlGn", vmin=-2, vmax=2, aspect="auto")
for i, row in enumerate(a["codes"]):
    for j, c in enumerate(row): ax.text(j, i, {"N": "중립", "?": "판독불가", "C": "부합", "wC": "약부합", "wI": "약불리"}[c], ha="center", va="center", fontsize=7)
ax.set_xticks(range(len(a["hypotheses"]))); ax.set_xticklabels(a["hypotheses"], fontsize=7, rotation=20, ha="right")
ax.set_yticks(range(len(a["evidence"]))); ax.set_yticklabels(a["evidence"], fontsize=7)
finish(ax, "그림 10. 경쟁가설 분석(ACH v2)", "사건 가설 H1–H5는 영상 증거로 서열을 매길 수 없다 — 진단력 있는 칸은 증거 계통 가설(H6·H7)뿐"); save(fig, "fig10_ach.png")
print("figures done")
