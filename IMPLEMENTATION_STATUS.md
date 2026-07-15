# 구현 상태

## 완료

- FastAPI/SQLAlchemy/SQLite 기본 구조
- 8개 JSON 통합 적재 스크립트와 1,393건 검증 로직
- 관광 콘텐츠 목록·상세·유형·지역·키워드·이미지 필터
- 위·경도 기반 가까운 콘텐츠 검색
- 익명 커뮤니티 CRUD와 비밀번호 확인
- API 응답 비밀번호 제외
- 데이터 출처/공공누리 제3유형 안내
- 규칙 기반 챗봇 fallback
- OpenAI Responses API function calling 선택 연동
- HTTP 관광 이미지 HTTPS 프록시와 화면 fallback
- Vue 홈·탐색·상세·커뮤니티·출처·플로팅 챗봇 화면
- Render Persistent Disk / Netlify 설정
- 백엔드 자동 테스트 6개

## 데이터 관련

현재 산출물에는 실행 확인용 데모 데이터만 생성하는 스크립트가 포함되어 있습니다. 실제 1,393건 원본 JSON은 `backend/app/data/raw/`에 배치한 뒤 아래 명령으로 적재합니다.

```bash
cd backend
python -m scripts.seed_database
```

적재 스크립트는 총건수, contentId 중복, 좌표 누락, 유형별 건수를 검증합니다.

## 검증 결과

- `pytest -q`: 6 passed
- `npm run build`: production build 성공
- 데모 적재 후 콘텐츠 API와 챗봇 fallback smoke test 성공
