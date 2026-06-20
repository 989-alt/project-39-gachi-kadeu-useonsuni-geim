# Fixes — cycle 1 (Dev → Tester)

## P1-A & P1-B (단일 패치로 해결)

`<style>` 최상단에 다음 한 줄 추가:

```css
[hidden] { display: none !important; }
```

이유: `prevBtn` / `memoSection`은 HTML `hidden` 속성으로 초기 상태를 표현하고 `render()` 가 `el.hidden = true/false` 로 토글한다. 그러나 `.btn { display: inline-flex }`, `.memo { display: flex }`가 같은 specificity로 `[hidden]`을 덮어쓴다. 표준 시맨틱인 `[hidden]`을 글로벌 우선시키는 `!important` 규칙으로 정렬. `display`만 덮어쓰므로 `.modal-backdrop[hidden] { display: none; }` 같은 기존 명시 룰과 충돌도 없음 (오히려 단순화 가능).

Tester에게 재검증 요청.
