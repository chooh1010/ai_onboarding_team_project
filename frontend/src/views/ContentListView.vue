<script setup>
import { onMounted, reactive, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { contentApi } from '../api/contentApi'
import ContentFilter from '../components/content/ContentFilter.vue'
import ContentList from '../components/content/ContentList.vue'

const route = useRoute()
const router = useRouter()
const types = ref([])
const areas = ref([])
const loading = ref(false)
const error = ref('')
const response = ref({
  items: [],
  page: 1,
  totalPages: 0,
  totalElements: 0,
})
const filters = reactive({
  contentTypeId: '',
  areaCode: '',
  sigunguCode: '',
  keyword: '',
  hasImage: null,
  page: 1,
  size: 12,
})

function syncFromRoute() {
  Object.assign(filters, {
    contentTypeId: route.query.contentTypeId || '',
    areaCode: route.query.areaCode || '',
    sigunguCode: route.query.sigunguCode || '',
    keyword: route.query.keyword || '',
    hasImage: route.query.hasImage === 'true' ? true : null,
    page: Number(route.query.page || 1),
    size: 12,
  })
}

async function load() {
  loading.value = true
  error.value = ''

  try {
    response.value = await contentApi.list(filters)
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

function search() {
  filters.page = 1
  router.push({
    query: Object.fromEntries(
      Object.entries(filters).filter(([, value]) => (
        value !== ''
        && value !== false
        && value !== null
        && value !== undefined
      )),
    ),
  })
}

function move(page) {
  router.push({ query: { ...route.query, page } })
}

onMounted(async () => {
  syncFromRoute()
  const [typeResponse, areaResponse] = await Promise.all([
    contentApi.types(),
    contentApi.areas(),
  ])
  types.value = typeResponse.items
  areas.value = areaResponse.items
  await load()
})

watch(
  () => route.query,
  async () => {
    syncFromRoute()
    await load()
  },
  { deep: true },
)
</script>

<template>
  <section class="page-hero explore-page-hero">
    <div class="container page-hero-inner">
      <div>
        <span class="page-hero-label">광주·전라 여행지 탐색</span>
        <h1>여행의 목적에 맞는 장소를<br />차분하게 골라보세요.</h1>
        <p>
          관광 유형, 지역, 장소명과 주소를 조합해 1,393개의 관광정보를 탐색할 수 있습니다.
        </p>
      </div>
      <div class="page-hero-decoration" aria-hidden="true">
        <span class="decor-sun" />
        <span class="decor-hill decor-hill-back" />
        <span class="decor-hill decor-hill-front" />
      </div>
    </div>
  </section>

  <section class="section explore-section">
    <div class="container">
      <ContentFilter
        v-model="filters"
        :types="types"
        :areas="areas"
        @search="search"
      />

      <div class="result-heading">
        <div>
          <span class="section-label">검색 결과</span>
          <strong>
            <template v-if="loading">장소를 찾고 있어요.</template>
            <template v-else>총 {{ response.totalElements.toLocaleString() }}개의 장소</template>
          </strong>
        </div>
        <span v-if="!loading" class="result-page-info">
          {{ Math.max(response.page, 1) }} / {{ Math.max(response.totalPages, 1) }} 페이지
        </span>
      </div>

      <div v-if="loading" class="content-loading" aria-live="polite">
        <span />
        <strong>관광정보를 불러오는 중입니다.</strong>
      </div>

      <div v-else-if="error" class="error-panel" role="alert">
        <strong>관광정보를 불러오지 못했습니다.</strong>
        <p>{{ error }}</p>
        <button type="button" class="button secondary" @click="load">다시 시도</button>
      </div>

      <ContentList v-else :items="response.items" />

      <nav
        v-if="!loading && response.totalPages > 1"
        class="pagination"
        aria-label="페이지 이동"
      >
        <button
          type="button"
          :disabled="response.page <= 1"
          @click="move(response.page - 1)"
        >
          <span aria-hidden="true">←</span> 이전
        </button>
        <span>
          <strong>{{ response.page }}</strong>
          <i>/</i>
          {{ response.totalPages }}
        </span>
        <button
          type="button"
          :disabled="response.page >= response.totalPages"
          @click="move(response.page + 1)"
        >
          다음 <span aria-hidden="true">→</span>
        </button>
      </nav>
    </div>
  </section>
</template>
