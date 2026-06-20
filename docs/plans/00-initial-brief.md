# Project #039 — 가치 카드 우선순위 게임 (도덕)

## 토픽
- **번호**: #039
- **제목**: 가치 카드 우선순위 게임
- **교과**: 도덕
- **대상**: 5~6학년 / 환경: 1:1
- **콘텐츠 주제·목표**: 정직·우정·자유 등 가치 카드 10장을 학생이 순서대로 정렬 → 5장으로 압축 → 3장으로 최종 압축. 자기 가치관 탐색.

## 원본 포함 기능
- 카드 드래그(랭킹 만들기)
- 단계별 압축 (10 → 5 → 3)
- 모둠 토의용 출력 (이름 없이 결과만)

## 원본 배제 기능
- 결과 외부 공유
- 학생 식별 결합

## 기술 결정
- **스택**: 단일 `index.html` + vanilla JS + 자기완비 vanilla CSS (CDN 의존 0).
  - 이유: drag-and-drop + 3단계 상태 머신 + canvas PNG export. React/Tailwind 오버킬.
  - Tailwind CDN 환경 차단 위험 회피.
- **Gemini API**: ✕ (원본 명세상 AI 옵션 없음).
- **저장**: 휘발성. PNG export만 외부 산출물.
- **i18n**: 한국어 단일.

## 디자인 브랜드
- design.md 기준 **Claude** (warm cream canvas + coral CTA + slab-serif display).
- 가치를 사색하는 분위기와 "editorial" 톤이 도덕 교과의 명상적 활동과 매치.

## 배포
- GitHub Pages, main 브랜치 root, 단일 HTML.
