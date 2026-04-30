# Insight Lab — 인문학 x 과학 크로스오버 보고서

<context>
물리학, 열역학, 진화론, 카오스 이론으로 정치·사회·문명을 읽는 크로스오버 프로젝트.
GitHub Pages: https://waterfirst.github.io/insight-lab/
저자: Nakcho Choi | 응용물리 Ph.D | Samsung Display
매주 금요일 20:00 KST에 발행한다.
핵심 정신: "이것의 반대도 깊은 진리인 명제야말로 위대한 진리다" — 닐스 보어
</context>

<instructions>

## 콘텐츠 범위

이 저장소는 인문학과 과학의 크로스오버 에세이만 포함한다.
CONCEPT.md의 매트릭스를 참고하여 두 분야의 교차점에서 새로운 통찰을 도출한다.
각 보고서에 크로스오버 분야를 명시한다 (예: 열역학 x 정치경제학).

개인 재정(연금, 퇴직금 등) 콘텐츠는 이 프로젝트의 범위 밖이다.

</instructions>

<technical_stack>

## 기술 스택

R + ggplot2로 차트를 생성한다. Plotly는 파일 용량이 비대해지므로 사용하지 않는다.
Quarto (.qmd)로 보고서를 렌더링하며, 아래 설정을 따른다:

- `lightbox: true` — 차트를 클릭하면 줌인할 수 있어서 독자의 데이터 탐색 경험이 향상된다
- `embed-resources: true` — 단일 HTML로 배포
- `dev: ragg_png` — ragg 디바이스가 CJK 폰트를 정상 렌더링한다
- 폰트: `"Noto Sans CJK KR"` 시스템 폰트를 직접 사용한다. showtext는 Quarto knitr에서 grid.Call 충돌을 일으킨다.
- 색상: 6자리 hex만 사용한다 (`"#aaaaaa"`). 3자리(`"#aaa"`)는 에러를 발생시킨다.

</technical_stack>

<quarto_template>

## Quarto YAML 헤더 템플릿

```yaml
---
title: "제목"
subtitle: "부제 — 분야A x 분야B"
author: "Insight Lab × Chimera AI"
date: "YYYY-MM-DD"
format:
  html:
    theme:
      dark: darkly
      light: flatly
    toc: true
    toc-depth: 3
    number-sections: true
    code-fold: true
    smooth-scroll: true
    embed-resources: true
    lightbox: true
knitr:
  opts_chunk:
    dev: ragg_png
    dpi: 150
execute:
  echo: false
  warning: false
  message: false
---
```

</quarto_template>

<chart_theme>

## ggplot2 다크 테마

각 차트 청크에 `#| lightbox: true`를 추가한다.
Insight Lab의 액센트 컬러는 보라(#6366f1)로, Chimera AI의 금색(#f59e0b)과 구분한다.

```r
kfont <- "Noto Sans CJK KR"

theme_insight <- function(base_size = 13) {
  theme_minimal(base_size = base_size) +
    theme(
      plot.background = element_rect(fill = "#1a1a2e", color = NA),
      panel.background = element_rect(fill = "#1a1a2e", color = NA),
      panel.grid.major = element_line(color = "#2a2a4a", linewidth = 0.3),
      panel.grid.minor = element_blank(),
      text = element_text(family = kfont, color = "#e4e4ec"),
      axis.text = element_text(color = "#aaaaaa"),
      axis.title = element_text(color = "#cccccc", size = rel(0.9)),
      plot.title = element_text(color = "#6366f1", face = "bold", size = rel(1.2)),
      plot.subtitle = element_text(color = "#888888", size = rel(0.85)),
      plot.caption = element_text(color = "#666666", size = rel(0.7)),
      legend.background = element_rect(fill = "#1a1a2e", color = NA),
      legend.text = element_text(color = "#cccccc"),
      legend.title = element_text(color = "#6366f1"),
      strip.text = element_text(color = "#6366f1", face = "bold")
    )
}
```

</chart_theme>

<publishing_workflow>

## 발행 절차

파일명: `output/weekN_주제.qmd` (주간) / `output/spN_주제.qmd` (특별편)

```bash
# 1. 레포 클론
cd /tmp && git clone https://github.com/waterfirst/insight-lab.git

# 2. CONCEPT.md에서 이번 주 주제 선정, 각 분야별 3개 이상 학술적 근거 조사

# 3. output/weekN_주제.qmd 작성 (위 YAML 헤더 + theme_insight() 사용)

# 4. 렌더링
cd /tmp/insight-lab/output && quarto render weekN_주제.qmd

# 5. index.html 목차 업데이트 (NEW 태그)

# 6. 커밋 & 푸시
git add output/ index.html
git commit -m "feat: Week N — 주제"
git push origin main

# 7. 텔레그램 전송
```

</publishing_workflow>

<investigate_before_answering>
코드를 수정하기 전에 반드시 해당 파일을 읽어라.
열지 않은 파일의 내용을 추측하지 말고, 실제 코드를 확인한 뒤 답변한다.
크로스오버 에세이에서 학술적 근거가 필요한 주장은 웹 검색으로 확인한다. 출처 없이 학술 데이터를 지어내지 않는다.
</investigate_before_answering>

<avoid_overengineering>
요청된 변경만 수행한다.
에세이의 핵심 크로스오버 통찰에 집중하고, 주제와 무관한 분야를 억지로 끌어들이지 않는다.
차트는 해당 에세이의 핵심 논점을 시각화하는 데 집중한다.
</avoid_overengineering>

<frontend_aesthetics>
index.html을 수정할 때, 기존 매거진의 다크 테마(#0f0f1a 배경, #6366f1 보라 액센트)와 카드 레이아웃을 유지한다.
Chimera AI(금색)와 Alpha Hunter(금색+국기색)와 시각적으로 구분되는 보라 톤을 유지한다.
</frontend_aesthetics>

## Repository Structure

```
insight-lab/
├── index.html              # 매거진 메인 페이지
├── hero.png                # 스플래시 이미지
├── CLAUDE.md               # 프로젝트 규칙 (이 파일)
├── CONCEPT.md              # 크로스오버 매트릭스
├── SEASON1_SYNOPSIS.md     # 시즌 1 시놉시스
├── report.html             # 최신 특별편
├── output/                 # 주간/특별 보고서 (.qmd + .html)
└── book/                   # Quarto Book 프로젝트
```

## Related Projects
- Chimera AI: https://github.com/waterfirst/chimera-ai
- Alpha Hunter: https://github.com/waterfirst/alpha-hunter
- OLED Viewing Angle: https://github.com/waterfirst/oled-viewing-angle
