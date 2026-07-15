<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const menuOpen = ref(false)

watch(
  () => route.fullPath,
  () => {
    menuOpen.value = false
  },
)
</script>

<template>
  <header class="site-header">
    <div class="container header-inner">
      <RouterLink to="/" class="brand" aria-label="남도온 홈">
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

      <button
        class="mobile-menu-button"
        type="button"
        :aria-expanded="menuOpen"
        aria-controls="primary-navigation"
        aria-label="메뉴 열기"
        @click="menuOpen = !menuOpen"
      >
        <span />
        <span />
        <span />
      </button>

      <div id="primary-navigation" :class="['header-navigation', { open: menuOpen }]">
        <nav aria-label="주요 메뉴">
          <RouterLink to="/explore">여행지 탐색</RouterLink>
          <RouterLink to="/community">여행 이야기</RouterLink>
          <RouterLink to="/data-source">데이터 안내</RouterLink>
        </nav>

        <RouterLink to="/explore" class="header-cta">
          여행 시작하기
          <span aria-hidden="true">→</span>
        </RouterLink>
      </div>
    </div>
  </header>
</template>
