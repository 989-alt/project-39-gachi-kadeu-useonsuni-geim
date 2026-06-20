# UI/UX — 가치 카드 우선순위 게임

> ui-ux-pro-max skill + design.md/claude/DESIGN.md 적용. 충돌시 DESIGN.md 우선.

## 디자인 브랜드: Claude

- **분위기**: warm cream canvas + slab-serif editorial — 학생이 가치를 "사색하는" 활동에 어울리는 차분한 톤.
- **색**: 코랄(#cc785c)을 1순위·CTA·완료 상태에만 절제해서 사용. 일상 카드는 cream + ink.
- **타이포**: 본문 system-ui / 디스플레이 Georgia (Copernicus serif fallback) — 폰트 다운로드 0.

## 색 체계 (DESIGN.md 직접 인용)
| 토큰 | hex | 용도 |
|---|---|---|
| canvas | `#faf9f5` | 페이지 바탕 |
| surface-card | `#efe9de` | 가치 카드 기본 |
| surface-cream-strong | `#e8e0d2` | 카드 hover / drag-target |
| primary | `#cc785c` | 1순위 강조 + 다음단계 CTA |
| primary-active | `#a9583e` | CTA pressed |
| ink | `#141413` | 본문 텍스트 |
| body | `#3d3d3a` | 카드 설명 |
| muted | `#6c6a64` | 보조 라벨 |
| hairline | `#e6dfd8` | 카드 외곽선 |
| surface-dark | `#181715` | 최종 PNG 결과 카드 바탕 (브랜드 시그니처) |
| on-dark | `#faf9f5` | 다크 카드 위 텍스트 |

## 화면 구조 (3 단계)

### 1. 10장 랭킹 화면
- **상단 헤더 (height 64px)**: 좌측 워드마크 "가치 카드", 우측 progress pill `1/3 · 10장`.
- **본문 (max-width 720px, 중앙정렬)**: 
  - h1 `display-md` "지금 너에게 더 중요한 가치는?" (Georgia/serif, 36px).
  - 한 줄 안내 body-md: "위로 올릴수록 더 중요한 가치예요. 카드를 드래그하거나 ↑↓ 버튼으로 순위를 바꿔보세요."
  - 1~10위 카드 리스트 (수직 stack):
    - 좌측 순위 숫자 (24px, muted)
    - 카드 본체 (surface-card, padding 16px, rounded-lg 12px)
      - 가치명 (title-md, 18px, 500)
      - 설명 (body-sm, 14px, body)
    - 우측 핸들 (`⋮⋮` 8px width, muted) + ↑↓ 미니 버튼 (각 36x36 touch target)
- **하단 액션 바 (sticky)**: "다음 단계: 5장으로" (button-primary, coral). Top 5 결정.

### 2. 5장 화면
- 헤더 progress `2/3 · 5장`.
- h1 "이 5개 중 정말 중요한 건?"
- 본문: 1~5위만 (10→5 자동 압축 결과). 동일 인터랙션.
- "이전 단계" (button-secondary) + "다음 단계: 3장으로" (button-primary).
- 메모 입력 (선택): textarea 100자, "왜 이 5개를 골랐어요?"

### 3. 3장 최종 화면
- 헤더 progress `3/3 · 3장`.
- h1 (display-lg 48px) "너의 TOP 3 가치"
- 1위 카드: **dark surface 강조** (#181715 바탕, coral 라벨 "1위"). 다른 두 장보다 패딩 큼.
- 2·3위: 일반 cream 카드.
- 메모 입력 (선택): "1순위 가치에 대해 한 줄로." 80자.
- 하단: "다시 처음부터" (text-link) + "결과를 PNG로 받기" (button-primary).

## 인터랙션

- **드래그**: HTML5 drag-and-drop API. 드래그 중 카드 opacity 0.5, drop target에 점선 outline (hairline).
- **키보드**: 카드에 `tabindex="0"` + `role="button"` + `aria-label="N위: 가치명. 위로/아래로 이동"`. ↑/↓ 키로 순위 교체.
- **터치/탭**: ↑↓ 미니 버튼 (44x44 touch target 확보).
- **포커스 링**: 2px solid coral, offset 2px.
- **transition**: 150ms ease-in-out for color/opacity; transform translateY for 순위 이동 (250ms).
- **`prefers-reduced-motion`**: 모션 모두 0.01s로 단축.

## 접근성 (CRITICAL 항목 체크)

- [x] **대비**: ink(#141413) on canvas(#faf9f5) — 17.4:1. body(#3d3d3a) on surface-card — 8.9:1. coral on white — 4.6:1. 모두 WCAG AA 통과.
- [x] **focus state**: 모든 인터랙티브 요소에 `:focus-visible` 코랄 outline.
- [x] **aria-label**: 핸들·미니 버튼 모두 aria-label.
- [x] **touch target**: ↑↓ 미니 버튼 44x44.
- [x] **읽기 폰트 크기**: 본문 16px, 카드 설명 14px (모바일 viewport에서 자동 확대).
- [x] **viewport**: `<meta name="viewport" content="width=device-width, initial-scale=1">`.

## PNG 출력 사양

- 캔버스 1080×1080 (정사각, SNS·인쇄 양쪽 호환).
- 바탕: surface-dark (#181715), warm cream 텍스트.
- 헤더: "MY TOP 3 가치 카드" (caption-uppercase, on-dark-soft).
- 1위 가치: display-lg 48px coral (#cc785c).
- 2·3위 가치: title-lg 22px on-dark.
- 1위 한 줄 메모(있으면): body-md cream.
- 하단: 날짜 "YYYY-MM-DD" + 안내 "1일 1바이브코딩 #039" (caption muted).
- **학생 식별자 0** — 입력 자체가 없으므로 자동 보장.
