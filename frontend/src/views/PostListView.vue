<script setup>
import { onMounted, reactive, ref } from 'vue'
import { postApi } from '../api/postApi'

const categories = [
  ['', '전체'],
  ['TOURISM', '관광지'],
  ['FOOD', '음식점·맛집'],
  ['LODGING', '숙박'],
  ['FESTIVAL', '축제·공연'],
  ['COURSE', '여행코스'],
  ['FREE', '자유'],
]

const filters = reactive({ category: '', keyword: '', page: 1, size: 10 })
const response = ref({ items: [], totalElements: 0, totalPages: 0, page: 1 })
const loading = ref(false)
const error = ref('')
const labels = Object.fromEntries(categories)

async function load() {
  loading.value = true
  error.value = ''
  try {
    response.value = await postApi.list(filters)
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

async function search() {
  filters.page = 1
  await load()
}

async function move(page) {
  filters.page = page
  await load()
}

onMounted(load)
</script>

<template>
  <section class="page-hero community-page-hero">
    <div class="container page-hero-inner">
      <div>
        <span class="page-hero-label">여행자의 목소리</span>
        <h1>남도를 먼저 다녀온 사람들과<br />편하게 이야기를 나눠보세요.</h1>
        <p>질문, 추천, 여행 경험을 익명으로 공유하는 광주·전라 여행 커뮤니티입니다.</p>
      </div>
      <RouterLink to="/community/write" class="button hero-community-button">
        여행 이야기 쓰기 <span aria-hidden="true">→</span>
      </RouterLink>
    </div>
  </section>

  <section class="section community-list-section">
    <div class="container">
      <div class="community-toolbar">
        <div class="category-tabs" aria-label="게시글 카테고리">
          <button
            v-for="[value, label] in categories"
            :key="value"
            type="button"
            :class="{ active: filters.category === value }"
            @click="filters.category = value; search()"
          >
            {{ label }}
          </button>
        </div>

        <form class="community-search" @submit.prevent="search">
          <span aria-hidden="true">⌕</span>
          <input v-model.trim="filters.keyword" placeholder="제목 또는 내용 검색" />
          <button class="button primary" type="submit">검색</button>
        </form>
      </div>

      <div class="community-list-heading">
        <div>
          <span class="section-label">여행 이야기</span>
          <strong>총 {{ response.totalElements.toLocaleString() }}개의 글</strong>
        </div>
        <RouterLink to="/community/write" class="button secondary">글쓰기</RouterLink>
      </div>

      <div v-if="loading" class="content-loading">
        <span />
        <strong>게시글을 불러오는 중입니다.</strong>
      </div>

      <div v-else-if="error" class="error-panel" role="alert">
        <strong>게시글을 불러오지 못했습니다.</strong>
        <p>{{ error }}</p>
        <button class="button secondary" type="button" @click="load">다시 시도</button>
      </div>

      <div v-else class="community-board">
        <RouterLink
          v-for="post in response.items"
          :key="post.id"
          :to="`/community/${post.id}`"
          class="community-row"
        >
          <span class="community-row-number">{{ String(post.id).padStart(2, '0') }}</span>
          <span class="category-chip">{{ labels[post.category] }}</span>
          <span class="community-row-title">{{ post.title }}</span>
          <span class="community-row-date">{{ new Date(post.createdAt).toLocaleDateString('ko-KR') }}</span>
          <span class="community-row-view">조회 {{ post.viewCount }}</span>
          <span class="community-row-arrow" aria-hidden="true">→</span>
        </RouterLink>

        <div v-if="!response.items.length" class="empty-state community-empty">
          <span class="empty-state-icon" aria-hidden="true">話</span>
          <strong>아직 등록된 게시글이 없습니다.</strong>
          <p>여행자들에게 첫 질문이나 경험을 남겨보세요.</p>
          <RouterLink to="/community/write" class="button primary">첫 글 작성하기</RouterLink>
        </div>
      </div>

      <nav v-if="response.totalPages > 1" class="pagination" aria-label="게시글 페이지 이동">
        <button type="button" :disabled="response.page <= 1" @click="move(response.page - 1)">
          <span aria-hidden="true">←</span> 이전
        </button>
        <span><strong>{{ response.page }}</strong><i>/</i>{{ response.totalPages }}</span>
        <button type="button" :disabled="response.page >= response.totalPages" @click="move(response.page + 1)">
          다음 <span aria-hidden="true">→</span>
        </button>
      </nav>
    </div>
  </section>
</template>
