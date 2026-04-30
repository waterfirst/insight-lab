# Insight Lab — 프로젝트 규칙

## Project Overview
- **인문학 x 과학 크로스오버 보고서** — 물리학, 열역학, 진화론, 카오스 이론으로 세상을 읽는다
- GitHub Pages: https://waterfirst.github.io/insight-lab/
- 저자: Nakcho Choi | 응용물리 Ph.D | Samsung Display

## Important Rules

### 1. 개인 연금 콘텐츠 금지
- **개인 연금(pension) 관련 콘텐츠는 이 프로젝트에 포함하지 않는다.**

## 기술 스택

### 필수 사항
- **R + ggplot2** — 차트 생성 (Plotly 사용 금지, 파일 용량 문제)
- **Quarto (.qmd)** — 보고서 렌더링
- `lightbox: true` — 차트 클릭 시 줌인
- `embed-resources: true` — 단일 HTML 배포
- `dev: ragg_png` — CJK 폰트 렌더링
- 폰트: `"Noto Sans CJK KR"` (시스템 폰트 직접 사용, showtext 사용 금지)

### 금지 사항
- **3자리 hex 색상 금지** — `"#aaa"` 사용 금지, 반드시 `"#aaaaaa"` 6자리 (Quarto+ragg 호환 문제)
- **showtext 사용 금지** — Quarto knitr 환경에서 충돌
- **Plotly 사용 금지** — 파일 용량 비대

### Quarto YAML 헤더 템플릿
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

### ggplot2 다크 테마 함수
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

### 파일 명명 규칙
```
output/weekN_주제.qmd / .html           # 주간 보고서
output/spN_주제.qmd / .html             # 특별편
```

### 보고서 필수 요소
- 각 차트 청크에 반드시 `#| lightbox: true` 추가
- 크로스오버 분야 명시 (예: 열역학 x 정치경제학)
- 닐스 보어 인용문: "이것의 반대도 깊은 진리인 명제야말로 위대한 진리다"

### 발행 절차
```bash
# 1. insight-lab 레포 클론
cd /tmp && git clone https://github.com/waterfirst/insight-lab.git

# 2. 주제 리서치 (CONCEPT.md 매트릭스 참조)

# 3. output/weekN_주제.qmd 작성 (위 YAML 헤더 사용)

# 4. Quarto 렌더링
cd /tmp/insight-lab/output
quarto render weekN_주제.qmd

# 5. index.html 목차 업데이트 (NEW 태그)

# 6. git commit & push origin main

# 7. cokacdir --sendfile로 텔레그램 전송
```

## Repository Structure
```
insight-lab/
├── index.html              # 매거진 메인 페이지 (목차)
├── hero.png                # 스플래시 이미지
├── CLAUDE.md               # 프로젝트 규칙 (이 파일)
├── CONCEPT.md              # 크로스오버 매트릭스
├── SEASON1_SYNOPSIS.md     # 시즌 1 시놉시스
├── report.html             # 최신 특별편 (TACO-Gibbs)
├── output/                 # 주간/특별 보고서
│   ├── weekN_주제.qmd / .html
│   └── spN_주제.qmd / .html
├── book/                   # Quarto Book 프로젝트
└── raw/                    # 원시 자료
```

## Related Projects
- Chimera AI: https://github.com/waterfirst/chimera-ai
- Alpha Hunter: https://github.com/waterfirst/alpha-hunter
- OLED Viewing Angle: https://github.com/waterfirst/oled-viewing-angle
