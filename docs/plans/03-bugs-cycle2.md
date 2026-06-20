# Bugs — cycle 2 (Tester → Dev)

자동 e2e 0 / 0 / 0 (console / pageerror / failed-request).

스크린샷 재검토:

## P1-C · stage 3 1위 다크 카드의 설명 문구가 2-3자마다 줄바꿈
- 재현: stage 3 진입 후 1위 카드(다크 surface). 설명 "다른 사람의 마음과 처지를 먼저 살펴요." 가 세로로 좁게 wrap.
- 원인: `.card`는 `grid-template-columns: 32px 1fr auto;` (3컬럼). stage 3 rank-1 override는 `48px 1fr` (2컬럼). 그러나 `.rank { display: none; }` 으로 첫 grid item이 사라지면, 두 번째 item인 `.card-body`가 grid auto-flow에 의해 첫 컬럼(48px)로 이동 → 좁아짐.
- P0/P1?: P1. 핵심 활동이 아닌 곁가지지만 1순위 가치 카드는 활동의 절정 화면이라 시각 임팩트가 떨어짐.
