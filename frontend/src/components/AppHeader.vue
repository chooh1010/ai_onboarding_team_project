<template>
  <header class="site-header">
    <div class="container header-inner">
      <RouterLink to="/" class="brand">
        <span class="brand-mark">남</span>
        <span>
          <strong>남도온</strong>
          <small>광주·전라권 여행정보</small>
        </span>
      </RouterLink>
      <nav aria-label="주요 메뉴">
        <RouterLink to="/explore">여행지 탐색</RouterLink>
        <RouterLink to="/community">여행 커뮤니티</RouterLink>
        <RouterLink to="/data-source">데이터 안내</RouterLink>
      </nav>
    </div>
  </header>
</template>
