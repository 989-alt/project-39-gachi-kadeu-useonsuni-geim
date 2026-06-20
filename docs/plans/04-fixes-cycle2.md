# Fixes — cycle 2 (Dev → Tester)

## P1-C

`.stage-3 .card.rank-1` 의 레이아웃을 grid → flex column 으로 바꿔서 auto-flow 의존성을 제거. ::before 의사요소도 자연스럽게 첫 flex 항목으로 흐름. card-body 자체도 내부 flex column으로 정렬, name과 desc가 컨테이너 전체 폭을 사용.

또한 1위 가치명은 serif 44px로 키우고, 부제(설명)는 16px on-dark-soft로 정돈. 1위·2위·3위의 시각 위계가 명확해짐.

Tester 재검증 결과 사이클 3 e2e + 시각 통과.
