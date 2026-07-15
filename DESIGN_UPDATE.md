# Product Hunt 스타일 디자인 개편

기준일: 2026-07-15

Product Hunt 2026년 7월 상위 제품 10개(Acti, Context.dev, AnySearch, ExploreYC, Fypro, Auriko, ChatCut, Glaze by Raycast, Sim, AgentKey)의 랜딩 페이지 흐름을 참고해 남도온의 화면을 재구성했습니다.

## 반영한 패턴

- 첫 화면에서 가치가 즉시 보이는 대형 헤드라인
- 검색 기능 자체를 제품 UI처럼 보여주는 히어로 프리뷰
- 떠 있는 반투명 내비게이션
- 짧고 분명한 CTA와 신뢰 지표
- 기능을 빠르게 훑을 수 있는 벤토 카드
- 어두운 배경과 라임·바이올렛 포인트 색상
- 큰 이미지와 간결한 메타정보 중심의 콘텐츠 카드
- 모바일에서 한 열로 자연스럽게 재배치되는 반응형 구조

## 주요 수정 파일

- `frontend/src/assets/main.css`
- `frontend/src/views/HomeView.vue`
- `frontend/src/views/ContentListView.vue`
- `frontend/src/components/AppHeader.vue`
- `frontend/src/components/AppFooter.vue`
- `frontend/src/components/content/ContentFilter.vue`
- `frontend/src/components/chat/ChatFloatingButton.vue`

기능 로직과 API 규격은 유지하고 시각 구조와 사용자 탐색 동선만 개편했습니다.
