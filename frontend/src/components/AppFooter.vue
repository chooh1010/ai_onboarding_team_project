<template>
  <footer class="site-footer">
    <div class="container footer-main">
      <div class="footer-intro">
        <RouterLink to="/" class="brand footer-logo" aria-label="남도온 홈">
          <span class="brand-mark" aria-hidden="true">
            <span class="brand-sun" />
            <span class="brand-hill brand-hill-back" />
            <span class="brand-hill brand-hill-front" />
          </span>
          <span class="brand-copy">
            <strong>남도온</strong>
            <small>광주·전라 여행을 한곳에</small>
          </span>
        </RouterLink>
        <p>
          관광지부터 음식점, 숙박과 여행자의 이야기까지.<br />
          남도의 오늘을 더 편안하게 발견하세요.
        </p>
      </div>

      <div class="footer-nav">
        <div>
          <strong>여행 탐색</strong>
          <RouterLink to="/explore">전체 여행지</RouterLink>
          <RouterLink to="/explore?contentTypeId=12">관광지</RouterLink>
          <RouterLink to="/explore?contentTypeId=39">음식점</RouterLink>
          <RouterLink to="/explore?contentTypeId=32">숙박</RouterLink>
        </div>
        <div>
          <strong>서비스</strong>
          <RouterLink to="/community">여행 커뮤니티</RouterLink>
          <RouterLink to="/community/write">여행 이야기 쓰기</RouterLink>
          <RouterLink to="/data-source">데이터 출처 안내</RouterLink>
        </div>
      </div>
    </div>

    <div class="container footer-source">
      <div>
        <strong>공공데이터 이용 안내</strong>
        <p>이 서비스는 한국관광공사 TourAPI 4.0 데이터를 활용하였습니다.</p>
      </div>
      <dl>
        <div>
          <dt>출처</dt>
          <dd>한국관광공사</dd>
        </div>
        <div>
          <dt>라이선스</dt>
          <dd>공공누리 제3유형</dd>
        </div>
      </dl>
    </div>

    <div class="container footer-bottom">
      <p>© 2026 Namdo On. 광주·전라권 관광정보 서비스</p>
      <p>원본 관광정보는 임의로 수정하지 않습니다.</p>
    </div>
  </footer>
</template>
