#!/usr/bin/env python3
"""
Insight Lab 주간 자동 생성기
매주 금요일 실행 → Quarto HTML + 음성 + 인포그래픽 생성
Bedrock Sonnet 사용 (Max 쿼터 절약)
"""
import os, sys, json, subprocess
from datetime import datetime
from pathlib import Path

# 경로 설정
BASE_DIR = Path("/home/ubuntu/.cokacdir/workspace/cp7jpheo/insight_lab")
OUTPUT_DIR = BASE_DIR / "output"
sys.path.insert(0, "/home/ubuntu")
from bedrock_helper import ask_bedrock

# Telegram 설정
TELEGRAM_TOKEN = "7927906835:AAFrilD2u3_maMK8uI5OMWVBJ_yA-Cj4U3Y"
CHAT_ID = "5767743818"

# 시즌 1 주제 (Week 1,2 완료)
SEASON1_TOPICS = {
    1: {"title": "양자역학 × 숙의 민주주의", "done": True},
    2: {"title": "열역학 × 제국의 흥망", "done": True},
    3: {
        "title": "진화론 × 기업 전략",
        "side_a": "다윈의 자연선택, 단속평형설, 적응 방산",
        "side_b": "시장 생존 조건, 점진적이지 않은 혁신, AI 시대 기업 적응",
        "done": False
    },
    4: {
        "title": "괴델의 불완전성 정리 × 법치주의",
        "side_a": "괴델 제1,2정리, 자기참조의 역설, 형식체계의 한계",
        "side_b": "법의 자기정당성, 헌법재판소의 역할, 법실증주의 vs 자연법론",
        "done": False
    },
    5: {
        "title": "카오스 이론 × 금융 위기",
        "side_a": "나비 효과, 프랙탈, 끌개(Attractor), 비선형 동역학",
        "side_b": "금융 시스템의 비선형성, 블랙스완, 시장 붕괴의 예측 불가능성",
        "done": False
    },
    6: {
        "title": "뇌과학 × 자유의지",
        "side_a": "리벳 실험, 무의식 의사결정, 양자 의식 가설",
        "side_b": "도덕적 책임, AI 감정의 자발성, 결정론 vs 자유의지",
        "done": False
    },
    7: {
        "title": "전염병 × 문명 전환",
        "side_a": "흑사병, 스페인 독감, 코로나, 전염병 역학",
        "side_b": "르네상스, 공중보건 체계, 디지털 전환, 문명 리셋 메커니즘",
        "done": False
    },
    8: {
        "title": "위상수학 × 도시 설계",
        "side_a": "쾨니히스베르크 다리, 네트워크 토폴로지, 오일러 특성수",
        "side_b": "교통망 최적화, SNS 정보 확산, 서울의 위상학적 구조",
        "done": False
    },
    9: {
        "title": "푸리에 변환 × 보안 철학",
        "side_a": "FFT, 신호 평균, 주파수 도메인, 중첩 원리, 노이즈 vs 신호",
        "side_b": "Google SynthID 워터마크 파훼, 투명성 vs 프라이버시, 창과 방패의 비대칭, 디지털 저작권의 한계",
        "done": False
    },
    10: {
        "title": "분산 시스템 × 기술 민주화",
        "side_a": "오케스트레이션, 샌드박싱, 오류 복구, 마이크로서비스 아키텍처",
        "side_b": "Anthropic Managed Agents, 4개월→8센트의 경제학, 인프라 장벽 붕괴, 플랫폼 경제의 진화",
        "done": False
    }
}

def get_current_week():
    """다음 진행할 주차 찾기"""
    for week, info in SEASON1_TOPICS.items():
        if not info.get("done", False):
            return week, info
    return None, None

def send_telegram(text):
    """Telegram 메시지 전송"""
    import requests
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"},
            timeout=15
        )
    except Exception as e:
        print(f"Telegram 전송 오류: {e}")

def send_file(filepath):
    """파일 전송 (cokacdir)"""
    try:
        result = subprocess.run([
            "/usr/local/bin/cokacdir",
            "--sendfile", filepath,
            "--chat", CHAT_ID,
            "--key", "2d09e87522bd6d28"
        ], capture_output=True, text=True, timeout=30)
        return result.returncode == 0
    except Exception as e:
        print(f"파일 전송 오류: {e}")
        return False

def generate_research_essay(week, topic_info):
    """Max 플랜 Opus로 딥 리서치 + 에세이 생성 (주 1회만, 품질 최우선)"""
    title = topic_info["title"]
    side_a = topic_info.get("side_a", "")
    side_b = topic_info.get("side_b", "")

    prompt = f"""당신은 인문학과 과학을 융합하는 리서치 전문가입니다.

이번주 주제: **{title}**

분야 A (과학): {side_a}
분야 B (인문/사회): {side_b}

아래 형식으로 **3000자 분량**의 깊이 있는 에세이를 작성하세요:

# {title}

## 서론: 왜 이 두 개념을 충돌시키는가

## 분야 A의 핵심 개념
- 3개의 핵심 메커니즘 또는 원리
- 각각에 대한 학술적 설명

## 분야 B의 핵심 이슈
- 현재 문제점 또는 질문
- 기존 설명의 한계

## 크로스오버: 분야 A로 분야 B를 재해석
- A의 개념이 B의 현상을 어떻게 설명하는가
- 기존 해석과 다른 인사이트 3가지
- 실제 사례 또는 데이터 근거

## 철학적 함의
- 이 크로스오버가 던지는 근본적 질문
- 인간 이해에 대한 새로운 시사점

## 실용적 적용
- 투자자/경영자에게 주는 교훈
- 정책 입안자에게 주는 제안
- 일상에 적용할 수 있는 프레임워크

## 미래 전망
- 이 크로스오버가 향후 5-10년간 어떻게 전개될 것인가

---

**톤**: 학술적이되 대중적, 단정적이되 열린, 깊이있되 명료하게.
**목표 독자**: 겐트대 송도 캠퍼스 학생/학부모, 과학기술 투자자, 인문학 애호가."""

    print(f"  Max 플랜 Opus로 Week {week} 에세이 생성 중...")
    # Opus는 Max 플랜 직접 사용 (주 1회만, 품질 최우선)
    import anthropic
    try:
        client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        msg = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        return msg.content[0].text
    except Exception as e:
        print(f"  Opus 실패, Bedrock Sonnet으로 폴백: {e}")
        return ask_bedrock(prompt, model="sonnet", max_tokens=4096)

def generate_quarto_html(week, title, essay):
    """Quarto HTML 보고서 생성"""
    qmd_path = OUTPUT_DIR / f"week{week}_{title.split(' ')[0].lower()}.qmd"
    html_path = OUTPUT_DIR / f"week{week}_{title.split(' ')[0].lower()}.html"

    qmd_content = f"""---
title: "Insight Lab Week {week}"
subtitle: "{title}"
author: "Nakcho Choi × Claude Opus 4.6"
date: "{datetime.now().strftime('%Y-%m-%d')}"
format:
  html:
    theme: cosmo
    toc: true
    toc-depth: 2
    code-fold: true
    self-contained: true
---

{essay}

---

_생성: {datetime.now().strftime('%Y-%m-%d %H:%M KST')} · Bedrock Sonnet · Insight Lab Season 1_
"""

    qmd_path.write_text(qmd_content, encoding="utf-8")
    print(f"  Quarto 렌더링: {qmd_path.name}")

    try:
        subprocess.run(
            ["quarto", "render", str(qmd_path)],
            cwd=str(OUTPUT_DIR),
            timeout=60,
            check=True
        )
        return html_path if html_path.exists() else None
    except Exception as e:
        print(f"  Quarto 렌더링 실패: {e}")
        return None

def generate_voice_essay(week, title, essay):
    """Edge TTS로 음성 에세이 생성"""
    # 3000자 에세이를 1500자로 요약
    summary_prompt = f"""아래 에세이를 **음성 낭독용**으로 1500자 이내로 요약하세요.
- 핵심 개념과 인사이트 3가지만 남기기
- 서론은 1-2문장으로 단축
- 학술 용어는 쉽게 풀어쓰기

{essay}"""

    print(f"  음성용 요약 생성 중...")
    voice_script = ask_bedrock(summary_prompt, model="haiku", max_tokens=2048)

    # 마크다운 제거
    voice_script = voice_script.replace("#", "").replace("*", "").replace("-", "")

    mp3_path = OUTPUT_DIR / f"week{week}_voice_essay.mp3"
    txt_path = OUTPUT_DIR / f"week{week}_voice_script.txt"
    txt_path.write_text(voice_script, encoding="utf-8")

    print(f"  Edge TTS 음성 생성 중...")
    try:
        subprocess.run([
            "edge-tts",
            "--voice", "ko-KR-SunHiNeural",
            "--text", voice_script,
            "--write-media", str(mp3_path)
        ], timeout=120, check=True)
        return mp3_path if mp3_path.exists() else None
    except Exception as e:
        print(f"  TTS 생성 실패: {e}")
        return None

def main():
    print(f"[{datetime.now()}] Insight Lab 주간 생성 시작")

    week, topic_info = get_current_week()
    if week is None:
        send_telegram("✅ Insight Lab 시즌 1 완료 (Week 1-8)")
        print("시즌 1 완료")
        return

    title = topic_info["title"]
    send_telegram(f"🧪 **Insight Lab Week {week}**\n주제: _{title}_\n생성 시작...")

    # 1. 에세이 생성
    essay = generate_research_essay(week, topic_info)

    # 2. Quarto HTML
    html_path = generate_quarto_html(week, title, essay)

    # 3. 음성 에세이
    mp3_path = generate_voice_essay(week, title, essay)

    # 4. 결과 전송
    success_msg = f"✅ **Week {week} 완료**\n_{title}_\n"

    if html_path and html_path.exists():
        send_file(str(html_path))
        success_msg += f"📄 HTML: {html_path.stat().st_size // 1024}KB\n"

    if mp3_path and mp3_path.exists():
        send_file(str(mp3_path))
        success_msg += f"🎧 음성: {mp3_path.stat().st_size // 1024}KB\n"

    success_msg += f"\n생성: {datetime.now().strftime('%H:%M KST')}"
    send_telegram(success_msg)

    # 5. 주제 완료 표시 (다음번 Week 4 실행하도록)
    SEASON1_TOPICS[week]["done"] = True

    print(f"Week {week} 생성 완료")

if __name__ == "__main__":
    main()
