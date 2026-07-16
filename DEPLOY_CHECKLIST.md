# 날씨·지도 배포 체크리스트

## Render 백엔드 환경변수

```env
OPENWEATHER_API_KEY=<OpenWeather 실제 키>
KAKAO_MAP_APP_KEY=<카카오 JavaScript 키>
BACKEND_CORS_ORIGINS=https://<프론트엔드-도메인>
```

환경변수 저장 후 백엔드 서비스를 재배포합니다.

## 프론트엔드 환경변수

Netlify 또는 Render Static Site의 **프론트엔드 서비스**에 설정합니다.

```env
VITE_API_BASE_URL=https://<백엔드-서비스>.onrender.com
```

변경 후 캐시를 지우고 새로 빌드·배포합니다. `VITE_API_BASE_URL` 끝에는 `/api`를 붙이지 않습니다.

## 카카오 개발자 콘솔

- JavaScript 키를 사용합니다.
- Kakao Map 사용 설정을 켭니다.
- JavaScript SDK 도메인에 실제 프론트엔드 주소를 등록합니다.

예:

```text
https://example.netlify.app
```

## 배포 후 확인

```text
https://<백엔드-서비스>.onrender.com/health
https://<백엔드-서비스>.onrender.com/api/config/public
https://<백엔드-서비스>.onrender.com/api/weather/current
```

`/api/config/public`에서 다음을 확인합니다.

- `openweatherConfigured: true`
- `kakaoMapAppKey`가 빈 문자열이 아님
