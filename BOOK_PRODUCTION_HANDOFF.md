# Insight Lab 두 번째 책 제작 바톤 문서

> 이 문서는 성능이 좋은 새 PC에서 Codex가 `insight-lab`의 기존 원고를 두 번째 단행본으로 완성하기 위한 실행 지침입니다.  
> 대상 저장소: <https://github.com/waterfirst/insight-lab>  
> 검증된 선행 출판 공정: <https://github.com/waterfirst/Debate-on-Semiconductor-Technology-and-the-Humanities/tree/22972631a277addf210ef4193a9147e55d90d9b2>  
> 작성일: 2026-08-17

## 0. 새 Codex가 가장 먼저 할 일

이 파일을 끝까지 읽고 저장소를 실제로 조사한 뒤 작업합니다. 기존 HTML·QMD·이미지를 읽지 않은 상태에서 내용을 추측하거나 대량 수정하지 않습니다.

새 PC에서 다음 순서로 시작합니다.

```powershell
git clone https://github.com/waterfirst/insight-lab.git
git clone https://github.com/waterfirst/Debate-on-Semiconductor-Technology-and-the-Humanities.git publishing-reference

cd publishing-reference
git checkout 22972631a277addf210ef4193a9147e55d90d9b2

cd ../insight-lab
git switch -c codex/insight-lab-book
```

Codex에는 다음 문장으로 작업을 시작시킵니다.

```text
BOOK_PRODUCTION_HANDOFF.md를 끝까지 읽고 그대로 수행하라.
먼저 insight-lab 전체 원고를 감사하고 책의 편집 방향 3개를 제안하라.
내가 방향을 선택하기 전에는 원고를 대량 수정하지 말라.
선택 이후에는 원고, 데이터, 삽화, 표지, PDF, EPUB, 검수 문서까지 완성하라.
선행 출판 저장소의 2297263 커밋에 있는 SKILL.md와 제작·검증 스크립트를 재사용하라.
```

## 1. 이번 책의 목표

Insight Lab에 축적된 과학·인문학 크로스오버 원고를 단순 묶음집이 아니라 **하나의 질문과 독서 흐름을 가진 대중 지식서**로 다시 편집합니다.

- 목표 독자: AI 시대의 인간·교육·노동·사회 변화를 깊이 이해하려는 20~50대 일반 독자
- 목표 분량: A5 본문 약 220~280쪽
- 발행처: `스칼라브릿지(Scholar Bridge)`
- 저자: `최낙초`
- 저자 소개: `응용물리학 박사, 반도체·디스플레이 제조업 25년차 엔지니어, Insight Lab 운영자`
- 금지 표기: 이전·현재 고용 회사의 실명, 특히 `Samsung Display` 또는 `삼성디스플레이`를 저자 소개에 사용하지 않습니다.
- 결과물: Quarto 원본, PDF 본문, 검토용 완성본, 인쇄용 날개 펼침표지, EPUB, README, SKILL, 출판 가이드, 검증 스크립트

## 2. 먼저 선택할 편집 방향

전체 원고를 한 권에 억지로 넣지 않습니다. Codex는 저장소 감사 뒤 아래 방향을 포함한 3개 기획안을 제시하고, 저자의 선택을 한 번 받습니다. 그 뒤에는 선택된 방향으로 자율적으로 완성합니다.

### A안 — 우선 추천

**가제:** 《AI 시대, 인간은 무엇으로 남는가》  
**부제:** 물리학·인지과학·경제학으로 다시 묻는 감정, 자유의지, 교육과 노동

핵심 원고 후보:

- `output/sp4_llm_emotion.qmd` — LLM 감정과 생명의 단층선
- `output/week6_free_will.qmd` — 뇌과학과 자유의지
- `output/sp6n_synthetic_humans.qmd` — 합성 인간과 사회학
- `output/sp12_ai_literacy.qmd` — AI 리터러시
- `output/c4_education_thermodynamics.qmd` — 교육과 AI 노동경제학
- `output/sp14_public_ai_paradox.qmd` — 공공 AI와 불평등
- `output/sp15_agent_control_room.qmd` — 에이전트와 인간의 통제
- `output/sp13_token_thermodynamics.qmd` — AI 비용의 물리학
- `output/sp10_impedance_neural.qmd` — 계면·신경망·AI 반도체
- `output/week1_quantum_democracy.qmd` — 숙의와 관찰
- `output/week4_godel_law.qmd` — 법과 형식체계의 한계
- `output/ss1_laws_game_theory.qmd` — 자율살상무기와 게임이론

장점은 주제가 응집되어 있고, AI·인문 교양서로 독자에게 설명하기 쉽다는 점입니다.

### B안

**가제:** 《경계에서 생각하는 법》  
**부제:** 양자역학·열역학·진화론·카오스로 다시 읽는 인간과 사회

Week 1~8의 대표 원고를 중심으로 과학 개념 하나와 사회 질문 하나를 장별로 교차합니다. Insight Lab의 정체성은 가장 잘 드러나지만, 장 사이 연결을 새로 써야 합니다.

### C안

**가제:** 《사회의 열역학》  
**부제:** 제국·시장·교육·AI 시스템은 왜 뜨거워지고 무너지는가

`week2`, `week5`, `c4`, `e1`, `sp5`, `sp13`, `sp14`, `sp15`를 중심으로 열역학·비선형 시스템·제어라는 하나의 언어로 묶습니다. 강한 콘셉트가 장점이지만, 과학적 비유의 적용 한계를 더 엄격히 써야 합니다.

## 3. 현재 저장소 감사 결과

### 출판 원고로 우선 사용할 것

- `output/*.qmd`: 완성도가 가장 높은 장문 원고의 기준 소스
- `raw/*.md`: 원고의 출발점과 출처 후보를 찾는 보조 자료
- `SEASON1_SYNOPSIS.md`: 전체 주제 지도와 누락된 장 파악
- `ROADMAP.md`: Insight Lab의 편집 원칙
- `CONCEPT.md`: 크로스오버 매트릭스
- `book/week01`, `book/week02`: 초기 Quarto Book 변환 사례

### 직접 출판 원고로 사용하지 않을 것

- `output/*.html`: 렌더링 결과이므로 본문 편집의 기준으로 삼지 않습니다.
- `report.html`, `index.html`: 웹 매거진용 파일이며 책 조판과 분리합니다.
- `output/metalens_idea.qmd`: 특허·기술 아이디어 성격이 강하므로 단행본 핵심 흐름에서 제외합니다.
- `output/sp6_taco_gibbs.qmd`: 정치·시장 시의성이 강합니다. 모든 사건과 수치를 새로 검증하지 못하면 제외하거나 별도 부록으로 돌립니다.
- `output/e1_coffee_thermodynamics.qmd`, `output/sp9_apple_metaphysics.qmd`: 본문 콘셉트에 맞을 때만 짧은 인터루드로 사용합니다.

현재 `book/`에는 Week 1·2만 들어 있습니다. 기존 웹 저널과 초기 `book/`을 보존하고, 새 단행본은 별도 `publication/` 폴더에서 만듭니다.

## 4. 새 책 폴더 구조

```text
publication/
  _quarto.yml
  index.qmd
  copyright.qmd
  preface.qmd
  recommendations.qmd        추천사 확정 뒤 포함
  epilogue.qmd
  author.qmd
  chapters/
    chapter01.qmd ...
  figures/
    data/
    illustrations/
  cover/
    front-cover-layout.svg
    back-cover-layout.svg
    full-wrap-layout.svg
    scholarbridge-logo.png
  scripts/
  output/
    pdf/
    epub/
```

기존 `book/`, `output/`, `raw/`는 원전 보존 영역으로 취급합니다. 원전 파일을 대량 수정하지 않고 `publication/chapters/`로 선별·재편집합니다.

## 5. 시행착오를 막는 전체 작업 순서

### 단계 1 — 기획 잠금

다음 다섯 항목을 먼저 확정합니다.

1. 제목과 부제
2. 핵심 독자 한 문장
3. 책 전체를 관통하는 중심 질문
4. 포함할 장 10~14개와 제외할 원고
5. 장별 역할과 순서

이 단계가 끝나기 전에는 표지 생성, 대량 문체 변환, PDF 조판을 하지 않습니다.

### 단계 2 — 원고 지도 작성

각 장에 대해 `원본 파일 → 핵심 질문 → 유지할 논지 → 새로 검증할 수치 → 삭제할 중복 → 필요한 도표·삽화` 표를 만듭니다. 같은 개념 설명이 여러 원고에 반복되면 최초 장에서만 충분히 설명하고 이후에는 짧게 참조합니다.

### 단계 3 — 사실 검증

- 학술 개념은 논문, 학회, 대학, 원전 등 1차 자료를 우선합니다.
- 통계는 정부·국제기구·기업 공시 등 공식 데이터로 확인합니다.
- 2025~2026년 정치·전쟁·기업·시장·AI 제품 관련 주장은 작업 당일 다시 검색합니다.
- 저장소에 있다는 이유만으로 날짜, 수치, 사건, 인용을 사실로 간주하지 않습니다.
- 확인할 수 없는 사례는 삭제하거나 가상 사고실험이라고 명시합니다.
- 직접 인용은 원문과 페이지를 확인하고 저작권상 필요한 최소 길이만 사용합니다.

특히 다음 표현은 자동으로 사실이 되지 않습니다.

- `과학이 증명한다`
- `구조가 완전히 같다`
- `필연적으로 붕괴한다`
- `AI는 감정을 느끼지 못한다`

증명, 모델, 구조적 유사성, 해석적 비유를 구분해 씁니다. 연결이 성립하지 않는 범위와 반대 해석을 반드시 포함합니다.

### 단계 4 — 장 구조 통일

각 장은 다음 기본 구조를 사용하되, 내용에 따라 1~2개 항목은 조정할 수 있습니다.

1. 독자를 끌어들이는 실제 장면 또는 사고실험
2. `경계의 질문` — 별도 글상자와 대비되는 서체
3. 첫 번째 학문의 개념과 근거
4. 두 번째 학문의 문제와 근거
5. 실제로 공유하는 구조
6. 비유가 깨지는 지점
7. 데이터 렌즈 — 그래프 또는 표
8. 대립하는 두 해석
9. 오늘의 사회·조직·개인에 주는 의미
10. 다음 장으로 이어지는 열린 질문
11. 출처와 주석

모든 장에 같은 체크리스트나 요약 상자를 반복하지 않습니다. 책 전체 체크리스트가 필요하면 에필로그 뒤에 한 번만 둡니다.

### 단계 5 — 문체 교정

- 설명문은 존댓말로 통일합니다.
- 학술적이되 한 번에 읽히는 문장을 사용합니다.
- 과도한 외래어, AI식 3단 병렬, 상투적 결론을 줄입니다.
- 한 문단에는 중심 주장 하나만 둡니다.
- 코드 문자, 깨진 기호, 잘못된 화살표, 문장 중간의 네모 문자를 전수 검색합니다.
- 장 제목에 수동 번호를 쓰지 않고 Quarto 번호만 사용합니다.
- 판권, 추천사, 서문, 에필로그, 저자 소개에는 장 번호를 붙이지 않습니다.
- 한두 글자만 다음 줄로 떨어지는 고아줄을 실제 PDF에서 수정합니다.

### 단계 6 — 데이터 시각화

- 막대그래프만 반복하지 않습니다.
- 시간 변화는 선그래프, 구성비는 도넛, 범주 비교는 세로 막대·롤리팝, 상관관계는 산점도, 판단 구조는 2×2 매트릭스를 우선합니다.
- 수치에는 단위, 기준 연도, 데이터 정의와 출처를 표시합니다.
- 비교할 수 없는 수치를 한 축에 합치지 않습니다.
- 표는 식별 열 약 28%, 설명 열 약 72%에서 시작해 A5 실제 폭으로 조정합니다.
- 내지 흑백 인쇄를 기준으로 색이 없어도 구분되도록 선 종류, 명도, 패턴을 함께 사용합니다.
- 기존 인터랙티브 Plotly 그래프를 인쇄용 정적 그래프로 다시 만듭니다.

### 단계 7 — 장별 삽화

이미지는 GPT Image 2를 사용하되, 한 책 안에서 다음 화풍을 고정합니다.

- 단색 연필 데생
- 옅은 수묵 번짐
- 따뜻한 백색 또는 한지 질감
- 한 장에 상징 한두 개
- 작은 A5 지면에서도 알아볼 수 있는 명확한 실루엣
- 이미지 안의 문자, 숫자, 로고, 워터마크 금지

각 장의 과학 개념과 인간적 질문이 하나의 장면에서 만나는 이미지를 만듭니다. 이미지를 생성한 뒤 여백, 중심축, 인쇄 시 명암을 눈으로 확인합니다. 판권면에는 저자의 기획·선정·편집과 생성형 AI 활용 사실을 한 번 고지합니다.

### 단계 8 — 한글 조판

선행 출판 저장소의 `book/print-style.tex`와 검증 스크립트를 출발점으로 사용합니다.

- 판형: A5 148 × 210mm
- 본문: Pretendard Regular 10~10.5pt
- 제목: Pretendard SemiBold
- `경계의 질문`: KoPub바탕 계열
- 줄 간격: 1.28~1.38 범위에서 실제 PDF로 결정
- 기본 여백: 안쪽 20mm, 바깥쪽 15mm, 위 18mm, 아래 20mm에서 시작
- 내지는 흑백, 백색모조 100g
- 본문에 재단까지 닿는 이미지가 없다면 A5 완성 크기로 제출하고, 내지 도련 필요 여부는 교보 최신 템플릿으로 확인

HTML에서 보기 좋은 레이아웃을 PDF에 그대로 옮기지 않습니다. 표, 수식, 코드, 각주, 캡션은 A5 인쇄 페이지에서 다시 설계합니다.

### 단계 9 — 표지와 Scholar Bridge 브랜드

표지 디자인은 본문 기획이 잠긴 뒤 시작합니다.

- 앞표지에는 제목과 핵심 상징을 우선하며 저자명·출판사명은 생략합니다.
- 뒤표지 왼쪽 아래에 Scholar Bridge 전체 로고를 둡니다.
- 뒤표지 오른쪽 아래에 ISBN/EAN-13 바코드 영역을 둡니다.
- 책등 아래에는 좁은 폭에 맞춰 `SCHOLAR BRIDGE` 워드마크를 작게 넣습니다.
- 판권면과 EPUB 메타데이터에는 `스칼라브릿지(Scholar Bridge)`를 씁니다.
- 로고는 선행 출판 저장소의 `book/cover/scholarbridge-logo.png`를 사용합니다.
- 표지는 컬러, 스노우 250g 우선, 무광 코팅을 기본값으로 하되 교보 등록 화면의 실제 옵션을 따릅니다.
- 날개는 좌우 80mm를 기본으로 합니다.
- 펼침표지 순서는 `왼쪽 날개 + 뒤표지 + 책등 + 앞표지 + 오른쪽 날개`입니다.
- 표지 사방 3mm 도련을 포함합니다.
- 책등 폭은 최종 본문 쪽수와 교보가 제공하는 종이별 계산값으로 마지막에 다시 정합니다.

이 책의 표지 콘셉트는 이전 책의 갓·웨이퍼 이미지를 반복하지 않습니다. 선택된 제목에 맞춰 `서로 다른 두 세계의 경계`, `인간과 기계의 단층선`, `과학 도식과 인간의 흔적` 중 하나를 단순한 상징으로 발전시킵니다. 밝은 톤과 썸네일 가독성을 우선합니다.

### 단계 10 — 추천사

추천사가 확정되기 전 파일은 `출간 후보본(RC)`으로 관리합니다.

- 추천인 이름·소속·직함과 최종 문안을 서면으로 확인합니다.
- 종이책, 전자책, 온라인 상품 소개에 게재할 수 있는지 확인합니다.
- 추천사는 판권면 다음, 서문 앞에 1~2쪽으로 배치합니다.
- 추천사 추가 뒤 PDF·EPUB·목차·쪽수·책등·펼침표지를 모두 다시 만듭니다.
- 판매 승인 뒤에는 쪽수 변경이 제한될 수 있으므로 추천사 마감 전에 교보 판매 신청을 하지 않습니다.

### 단계 11 — 렌더링과 검수

Quarto는 형식별 렌더링 때 `_book`을 갱신할 수 있으므로 EPUB을 먼저 만들고 안정된 폴더로 복사한 뒤 PDF를 만듭니다.

```powershell
cd publication
quarto render . --to epub
Copy-Item "_book/*.epub" "output/epub/" -Force
quarto render . --to pdf
python cover/build_cover_pdfs.py
cd ..
uv run --with pypdf python publication/scripts/verify_publish_artifacts.py
```

검수는 세 단계로 수행합니다.

1. **구조 검수:** 장 수, 목차, 번호, 존댓말, 중복, 출처
2. **시각 검수:** 서문, 판권, 긴 장 제목, 모든 장 첫 페이지, 표, 그래프, 삽화, 에필로그, 저자 소개
3. **산출물 검수:** A5 크기, 페이지 수, PDF 메타데이터, EPUB 메타데이터, 책등, 3mm 표지 도련, TrimBox

PDF는 반드시 페이지 이미지로 렌더링해 눈으로 봅니다. 자동 검증 통과만으로 출판 완료라고 판단하지 않습니다.

## 6. 선행 출판 저장소에서 재사용할 파일

다음 파일을 그대로 복사한 뒤 경로와 책 제목만 새 프로젝트에 맞게 수정합니다.

- `SKILL.md` — 전체 Quarto 한국어 출판 공정
- `KYOBO_PUBLISHING_GUIDE.md` — 교보 POD·전자책 등록 절차
- `book/print-style.tex` — A5 한글 조판
- `book/cover/build_cover_pdfs.py` — 본문·표지 결합과 펼침표지 출력
- `scripts/render_cover_assets.mjs` — SVG 표지 렌더링
- `scripts/formalize_korean.mjs` — 존댓말 점검
- `scripts/verify_publish_artifacts.py` — PDF·EPUB 판형·메타데이터 검증
- `book/cover/scholarbridge-logo.png` — 출판사 로고

복사 뒤에는 이전 책 제목, 반도체 면접 전용 문구, 224쪽·14mm 같은 고정값이 남아 있지 않은지 검색합니다.

```powershell
rg -n "반도체 면접|왕의 질문|224|14mm|삼성디스플레이|Samsung Display" publication README.md SKILL.md
```

## 7. 새 PC 준비 체크리스트

- [ ] Git과 저장소 인증이 준비되었습니다.
- [ ] Quarto 최신 안정 버전이 설치되었습니다.
- [ ] TinyTeX 또는 TeX Live와 XeLaTeX가 설치되었습니다.
- [ ] Pretendard와 KoPub 계열 한글 폰트가 설치되었습니다.
- [ ] Python과 `pypdf`, `pypdfium2`, `reportlab`, `pdfplumber`를 사용할 수 있습니다.
- [ ] Node.js와 `sharp`를 사용할 수 있습니다.
- [ ] 기존 R 차트를 재사용한다면 R, `ggplot2`, `tidyverse`, `ragg`, 필요한 패키지를 설치했습니다.
- [ ] Codex에서 PDF와 이미지 생성 스킬을 사용할 수 있습니다.
- [ ] Scholar Bridge 로고 원본을 확보했습니다.

설치 직후 작은 샘플 PDF·EPUB·PNG를 각각 한 번 만들어 도구 체인을 확인한 뒤 본문 전체 렌더링을 시작합니다.

## 8. 출판 직전 최종 상태

다음 파일이 모두 있어야 출판 준비 완료입니다.

```text
publication/output/pdf/<책제목>-본문-A5.pdf
publication/output/pdf/<책제목>-최종본.pdf
publication/output/pdf/<책제목>-인쇄용-펼침표지.pdf
publication/output/epub/<책제목>.epub
publication/cover/front-cover-final.png
README.md
SKILL.md
KYOBO_PUBLISHING_GUIDE.md
```

ISBN, 정가, 발행일이 미정이면 판권면에 임의 값을 넣지 않습니다. 실제 ISBN을 받은 뒤 뒤표지의 빈 바코드 영역을 EAN-13 바코드로 교체하고 마지막 렌더링을 합니다. 종이책과 전자책은 각각 별도의 ISBN을 사용합니다.

## 9. Git 작업 원칙

- 기존 `main`의 저널·웹페이지를 훼손하지 않습니다.
- `codex/insight-lab-book` 브랜치에서 책을 완성하고 검수합니다.
- 사용자가 전체 시안을 승인한 뒤 `main`에 병합합니다.
- 원고, 표지 원본, 최종 PDF, EPUB, README, SKILL, 출판 가이드를 함께 커밋합니다.
- 임시 렌더링 파일, `_freeze`, `_book` 중간 산출물, 개인 경로와 비밀키는 커밋하지 않습니다.
- 큰 HTML 파일을 새로 복제하지 않고 필요한 QMD·데이터·정적 이미지만 사용합니다.
- 커밋 전 `git status`, `git diff --check`, 렌더링, PDF 자동 검증을 실행합니다.

## 10. 작업 완료의 정의

아래 조건을 모두 충족해야 “완료”라고 보고합니다.

- [ ] 제목·부제·독자·목차가 한 방향으로 연결됩니다.
- [ ] 각 장의 두 학문이 실제 분석에 기여하고 단순 장식적 비유가 아닙니다.
- [ ] 최신 수치와 시사 사례가 1차 자료로 검증되었습니다.
- [ ] 존댓말, 번호, 글자 간격, 고아줄, 표와 그래프가 교정되었습니다.
- [ ] 장별 삽화가 한 화풍으로 통일되고 흑백 인쇄에서 읽힙니다.
- [ ] 앞표지, 뒤표지, 책등, 양쪽 날개가 하나의 디자인으로 완성되었습니다.
- [ ] Scholar Bridge 로고와 명칭이 정해진 위치에 있습니다.
- [ ] PDF·EPUB·인쇄용 펼침표지가 모두 생성되고 자동·시각 검수를 통과했습니다.
- [ ] 추천사 또는 추천사 미수록 방침이 확정되었습니다.
- [ ] ISBN·바코드·정가·발행일을 제외한 출판 정보가 완성되었습니다.
- [ ] README, SKILL, 교보 출판 가이드가 현재 책에 맞게 갱신되었습니다.
- [ ] 모든 변경이 GitHub에 안전하게 반영되었습니다.

## 11. 현재 바톤 상태

- `insight-lab`의 기존 저널 원고는 그대로 보존되어 있습니다.
- 새 단행본의 실제 편집 작업은 아직 시작하지 않았습니다.
- 다음 Codex의 첫 산출물은 **저장소 원고 감사표와 3개 편집 기획안**입니다.
- 저자가 기획안을 선택하면 `publication/` 생성부터 최종 출판 파일까지 한 흐름으로 진행합니다.

