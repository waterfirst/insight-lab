#!/usr/bin/env python3
"""저널 목차 카드에 NotebookLM 오디오 링크를 붙이고 발행까지 한다.

사용:
    python3 tools/add_audio.py sp26 "<NotebookLM 공유 URL>"        # 붙이고 발행
    python3 tools/add_audio.py sp26 "<URL>" --dry                  # 확인만

왜 도구로 만들었나 (2026-09-27):
  손으로 하면 매번 틀릴 자리가 네 곳이다.
    1) 카드가 NEW·완료 두 곳에 있다 — 한쪽만 붙이면 필터 상태에 따라 오디오가 사라진다
    2) .cr cc 안, 크로스오버 라벨 '뒤'에 와야 한다
    3) stopPropagation 이 없으면 오디오를 눌렀는데 기사로 튄다
    4) utm 은 art_share_1 까지만 — 뒤쪽 추적 파라미터를 지운다
  두 번째 오디오를 붙이면 기존 것을 'Audio 1'로 고치고 새 것을 'Audio 2'로 만든다.
  삽입이 2곳이 아니면 무조건 중단한다.
"""
import re, subprocess, sys, time, shutil, datetime
from pathlib import Path
from urllib.request import urlopen

REPO = Path(__file__).resolve().parent.parent
IDX = REPO / "index.html"
LIVE = "https://waterfirst.github.io/insight-lab/"
SVG = ('<svg viewBox="0 0 24 24"><path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55'
       'C7.79 13 6 14.79 6 17s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/></svg>')

def sh(*a, **kw):
    return subprocess.run(a, cwd=REPO, text=True, capture_output=True, **kw)

def btn(url, label="Audio"):
    return (f'<a href="{url}" target="_blank" rel="noopener" class="audio-btn" '
            f'onclick="event.stopPropagation()">{SVG}{label}</a>')

def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    slug, url = sys.argv[1], sys.argv[2]
    dry = "--dry" in sys.argv

    # utm 은 art_share_1 까지만 남긴다
    url = re.sub(r"(utm_campaign=art_share_1).*$", r"\1", url.strip())
    if "notebook.google.com" not in url:
        sys.exit(f"🔴 NotebookLM 공유 URL 이 아니다: {url[:60]}")
    aid = re.search(r"/artifact/([0-9a-f-]{8,})", url)
    if not aid:
        sys.exit("🔴 URL 에 /artifact/<id> 가 없다 — 오디오 공유 링크인지 확인하라")
    aid = aid.group(1)

    s = IDX.read_text(encoding="utf-8")
    if aid in s:
        sys.exit(f"이미 붙어 있다 (artifact {aid[:8]}). 아무것도 바꾸지 않았다.")

    lines, n = s.split("\n"), 0
    for i, ln in enumerate(lines):
        if not (re.search(rf'href="output/{slug}_[^"]*\.html"', ln) and 'class="cd"' in ln):
            continue
        end = "</div></a></div>"
        if not ln.endswith(end):
            sys.exit(f"🔴 카드 끝 형식이 예상과 다르다 (줄 {i+1}): ...{ln[-40:]}")
        have = ln.count("audio-btn")
        if have:                       # 기존 것을 Audio 1 로 바꾸고 새 것은 다음 번호
            if ">Audio</a>" in ln:
                ln = ln.replace(">Audio</a>", ">Audio 1</a>")
            label = f"Audio {have + 1}"
        else:
            label = "Audio"
        lines[i] = ln[:-len(end)] + btn(url, label) + end
        n += 1

    if n != 2:
        sys.exit(f"🔴 중단 — {slug} 카드를 {n}곳 찾았다 (NEW·완료 2곳이어야 한다)")

    print(f"{slug} 카드 2곳에 '{label}' 삽입 예정 · artifact {aid[:8]}")
    if dry:
        print("--dry 이므로 파일을 바꾸지 않았다."); return

    shutil.copy2(IDX, REPO / f"index.html.bak-{datetime.datetime.now():%Y%m%dT%H%M%SZ}")
    IDX.write_text("\n".join(lines), encoding="utf-8")

    p = sh("git", "pull", "--ff-only", "origin", "main")
    if p.returncode: sys.exit(f"🔴 pull 실패:\n{p.stderr[-400:]}")
    sh("git", "add", "index.html")
    staged = sh("git", "diff", "--cached", "--name-only").stdout.split()
    if staged != ["index.html"]:
        sys.exit(f"🔴 스테이징이 index.html 하나가 아니다: {staged}")
    msg = (f"{slug.upper()} 목차 카드에 NotebookLM 오디오 링크 추가\n\n"
           f"NEW·완료 두 카드 모두. .cr cc 안 크로스오버 라벨 뒤, stopPropagation 으로\n"
           f"카드 클릭과 분리. utm 은 art_share_1 까지만 남겼다.\n\n"
           f"Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>\n")
    p = sh("git", "commit", "-q", "-m", msg)
    if p.returncode: sys.exit(f"🔴 commit 실패:\n{p.stderr[-400:]}")
    p = sh("git", "push", "origin", "main")
    if p.returncode: sys.exit(f"🔴 push 실패:\n{p.stderr[-400:]}")
    print("푸시 완료 — 라이브 확인 중 (최대 150초)")

    for k in range(15):
        time.sleep(10)
        try:
            body = urlopen(LIVE, timeout=12).read().decode("utf-8", "replace")
        except Exception:
            continue
        c = body.count(aid)
        print(f"  [{(k+1)*10}s] 라이브 오디오 링크 {c}개")
        if c >= 2:
            print("✅ 발행 확인"); return
    print("⚠️ 150초 안에 확인되지 않았다 — Pages 빌드가 느릴 수 있다. 잠시 후 다시 확인하라.")

if __name__ == "__main__":
    main()
