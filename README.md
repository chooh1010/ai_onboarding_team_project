# 광주·전라권 관광정보 서비스

한국관광공사 TourAPI 4.0 기반 관광 콘텐츠 검색, 익명 커뮤니티, 관광 안내 챗봇을 제공하는 FastAPI + Vue 3 프로젝트입니다.

## 구현 범위

- 관광 콘텐츠 유형/지역/키워드/이미지 보유 여부 검색
- 콘텐츠 상세 및 좌표 기반 가까운 장소 검색
- 익명 커뮤니티 CRUD와 비밀번호 확인
- 데이터 출처/라이선스 안내
- 데이터 한계를 지키는 규칙 기반 챗봇 fallback
- `OPENAI_API_KEY`가 있을 때 Responses API function calling 사용
- HTTP 원본 이미지용 HTTPS 프록시와 이미지 fallback
- FastAPI 테스트
- Render/Netlify 배포 설정 예시

## 1. 데이터 배치

아래 8개 원본 JSON을 `backend/app/data/raw/`에 넣습니다.

```text
광주_전라권_관광지.json
광주_전라권_레포츠.json
광주_전라권_문화시설.json
광주_전라권_쇼핑.json
광주_전라권_숙박.json
광주_전라권_여행코스.json
광주_전라권_음식점.json
광주_전라권_축제공연행사.json
```

원본 주소, 이미지 URL, 분류 값은 수정하지 않고 `raw_json`에도 그대로 보존합니다.

## 2. 백엔드 실행

```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
python -m scripts.seed_database
uvicorn app.main:app --reload
```

- API 문서: `http://localhost:8000/docs`
- 헬스체크: `http://localhost:8000/health`

실제 JSON 없이 화면 흐름만 확인할 때는 다음 데모 데이터를 사용할 수 있습니다.

```bash
python -m scripts.seed_demo_database
```

## 3. 프론트엔드 실행

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

기본 주소는 `http://localhost:5173`입니다.

## 4. 테스트

```bash
cd backend
pytest -q
```

## 5. 환경 변수

백엔드 주요 변수:

```env
DATABASE_URL=sqlite:///./regional_tour.db
BACKEND_CORS_ORIGINS=http://localhost:5173
OPENAI_API_KEY=
OPENAI_MODEL=gpt-5-mini
OPENWEATHER_API_KEY=
KAKAO_MAP_APP_KEY=
```

프론트엔드:

```env
VITE_API_BASE_URL=http://localhost:8000
# 선택 사항: 비워두면 백엔드 KAKAO_MAP_APP_KEY를 사용
VITE_KAKAO_MAP_APP_KEY=
```

> `OPENWEATHER_API_KEY`가 없으면 날씨 API가 동작하지 않습니다.
> `KAKAO_MAP_APP_KEY`에는 카카오 **JavaScript 키**를 넣고, 카카오 개발자 콘솔에 실제 프론트엔드 배포 도메인을 등록해야 합니다.
> Netlify/Render Static Site에서 `VITE_API_BASE_URL`을 바꾼 뒤에는 프론트엔드를 다시 빌드·배포해야 합니다.

## 6. 배포 확인 주소

백엔드 배포 후 아래 주소를 브라우저에서 직접 확인합니다.

```text
https://<백엔드-주소>/health
https://<백엔드-주소>/api/config/public
https://<백엔드-주소>/api/weather/current
```

- `/api/config/public`의 `openweatherConfigured`가 `true`여야 합니다.
- `kakaoMapAppKey`가 비어 있으면 Render의 `KAKAO_MAP_APP_KEY`를 확인합니다.
- 프론트엔드에는 `VITE_API_BASE_URL=https://<백엔드-주소>`가 필요합니다.

## 주의

과제 명세에 맞춰 커뮤니티 수정·삭제 비밀번호를 평문으로 저장합니다. 실제 서비스에서는 반드시 Argon2 또는 bcrypt 같은 단방향 해시를 적용해야 합니다.

축제 시작일·종료일은 축제공연행사 JSON의 값을 사용합니다. 모범음식점 지정 여부, 여행코스 상세 경로, 메뉴·가격·영업시간처럼 데이터에 없는 정보는 서비스와 챗봇이 추측하지 않습니다.

## 데이터 출처

이 서비스는 한국관광공사 TourAPI 4.0 데이터를 활용합니다.

- 출처: 한국관광공사
- 라이선스: 공공누리 제3유형
- 원본 데이터 내용 변경 금지
