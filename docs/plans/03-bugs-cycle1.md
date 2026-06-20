# Bugs — cycle 1 (Tester → Dev)

> 자동 e2e 자체는 통과 (console 0 / pageerror 0 / failed-request 0). 그러나 스크린샷 검토에서 시각적 P1 결함 2건 발견.

## P1-A · stage 1에서 "이전 단계" 버튼이 보임
- 재현: index.html 로드 직후 스크롤하면 fixed actionbar에 `← 이전 단계` 버튼이 노출.
- 기대: stage 1에서는 `prevBtn`이 숨겨져야 함 (브리프상 "이전 단계"는 stage 2부터).
- 원인: `<button class="btn btn-link" id="prevBtn" hidden>` 에서 HTML `hidden` 속성은 `display:none`를 의도하지만, CSS `.btn { display: inline-flex; }` 가 `[hidden]` 규칙과 같은 specificity (둘 다 0,1,0) 이고 뒤에 선언돼 이긴다.
- 동일 root cause로 `<section class="memo" id="memoSection" hidden>` 도 stage 1에서 노출됨 — 화면 하단에 메모 입력칸과 글자수 카운터가 보임. 학생 혼동 가능.

## P1-B · stage 1 메모 영역 노출
- P1-A와 같은 specificity 충돌. `.memo { display: flex; }` 가 `[hidden]`을 덮음.

## 권장 픽스
- 전역 `[hidden] { display: none !important; }` 추가 (HTML5 표준 시맨틱이라 `!important` 합당).
- 또는 좀 더 좁게: `.btn[hidden]`, `.memo[hidden]` 명시. 전자가 안전.
