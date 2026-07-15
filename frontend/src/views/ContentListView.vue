<script setup>
import { onMounted, reactive, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { contentApi } from '../api/contentApi'
import ContentFilter from '../components/content/ContentFilter.vue'
import ContentList from '../components/content/ContentList.vue'
import ContentMap from '../components/content/ContentMap.vue'

const route = useRoute()
const router = useRouter()
const types = ref([])
const areas = ref([])
const loading = ref(false)
const response = ref({ items: [], page: 1, totalPages: 0, totalElements: 0 })

// 지도에 전달할 항목을 별도로 유지 (한 번에 더 많이 로드)
const mapItems = ref([])

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
  try {
    response.value = await contentApi.list(filters)
  } finally {
    loading.value = false
  }
}

// 지도에 표시할 데이터를 별도 로드 (page=1, size=100 등)
async function loadMapItems() {
  try {
    // copy filters but request more items for map (do not mutate original filters)
    const params = {
      contentTypeId: filters.contentTypeId,
      areaCode: filters.areaCode,
      sigunguCode: filters.sigunguCode,
      keyword: filters.keyword,
      hasImage: filters.hasImage,
      page: 1,
      size: 100, // 지도에 최대 100개(원하면 더 변경)
    }
    const mapResp = await contentApi.list(params)
    mapItems.value = mapResp.items || []
  } catch (err) {
    // 실패해도 리스트 동작에는 영향 없게 처리
    console.error('loadMapItems failed', err)
    mapItems.value = []
  }
}

function search() {
  filters.page = 1
  router.push({
    query: Object.fromEntries(
      Object.entries(filters).filter(
        ([, value]) => value !== '' && value !== false && value !== null
      )
    ),
  })
}

function move(page) {
  router.push({ query: { ...route.query, page } })
}

function goToDetail(item) {
  if (item?.contentId) {
    router.push(`/contents/${item.contentId}`)
  }
}

onMounted(async () => {
  syncFromRoute()
  const [typeResponse, areaResponse] = await Promise.all([contentApi.types(), contentApi.areas()])
  types.value = typeResponse.items
  areas.value = areaResponse.items
  await load()
  await loadMapItems() // 지도용 데이터 별도 로드
})

watch(
  () => route.query,
  async () => {
    syncFromRoute()
    await load()
    await loadMapItems() // 라우트 변경 시 지도 데이터도 갱신
  },
  { deep: true }
)
</script>

<template>
  <section class="page-hero compact">
    <div class="container">
      <p class="eyebrow">Explore</p>
      <h1>여행지 탐색</h1>
      <p>유형과 지역, 검색어를 조합해 원하는 장소를 찾아보세요.</p>
    </div>
  </section>

  <section class="section container">
    <ContentFilter v-model="filters" :types="types" :areas="areas" @search="search" />
    <!-- 지도에는 mapItems 전달 -->
    <ContentMap :items="mapItems" :total-count="response.totalElements" @select-item="goToDetail" />

    <div class="result-heading">
      <strong>총 {{ response.totalElements.toLocaleString() }}건</strong>
      <span v-if="loading">불러오는 중…</span>
    </div>

    <ContentList :items="response.items" />

    <nav v-if="response.totalPages > 1" class="pagination" aria-label="페이지 이동">
      <button :disabled="response.page <= 1" @click="move(response.page - 1)">이전</button>
      <span>{{ response.page }} / {{ response.totalPages }}</span>
      <button :disabled="response.page >= response.totalPages" @click="move(response.page + 1)">다음</button>
    </nav>
  </section>
</template>