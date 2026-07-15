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
const response = ref({ items: [], page: 1, totalPages: 0, totalElements: 0 })
const filters = reactive({ contentTypeId: '', areaCode: '', sigunguCode: '', keyword: '', hasImage: null, page: 1, size: 12 })

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

function search() {
  filters.page = 1

  router.push({
    query: Object.fromEntries(
      Object.entries(filters).filter(
        ([, value]) =>
          value !== '' &&
          value !== false &&
          value !== null
      )
    ),
  })
}

function move(page) {
  router.push({ query: { ...route.query, page } })
}

onMounted(async () => {
  syncFromRoute()
  const [typeResponse, areaResponse] = await Promise.all([contentApi.types(), contentApi.areas()])
  types.value = typeResponse.items
  areas.value = areaResponse.items
  await load()
})
watch(() => route.query, async () => { syncFromRoute(); await load() }, { deep: true })
</script>

<template>
  <section class="page-hero compact"><div class="container"><p class="eyebrow">Explore</p><h1>여행지 탐색</h1><p>유형과 지역, 검색어를 조합해 원하는 장소를 찾아보세요.</p></div></section>
  <section class="section container">
    <ContentFilter v-model="filters" :types="types" :areas="areas" @search="search" />
    <div class="result-heading"><strong>총 {{ response.totalElements.toLocaleString() }}건</strong><span v-if="loading">불러오는 중…</span></div>
    <ContentList :items="response.items" />
    <nav v-if="response.totalPages > 1" class="pagination" aria-label="페이지 이동">
      <button :disabled="response.page <= 1" @click="move(response.page - 1)">이전</button>
      <span>{{ response.page }} / {{ response.totalPages }}</span>
      <button :disabled="response.page >= response.totalPages" @click="move(response.page + 1)">다음</button>
    </nav>
  </section>
</template>
