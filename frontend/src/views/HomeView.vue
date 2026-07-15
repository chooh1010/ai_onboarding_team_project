<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { contentApi } from '../api/contentApi'
import { postApi } from '../api/postApi'
import ContentList from '../components/content/ContentList.vue'

const router = useRouter()
const keyword = ref('')
const types = ref([])
const featured = ref({ tourism: [], food: [], lodging: [] })
const posts = ref([])

const typeIcons = { '12': '산', '14': '문', '15': '축', '25': '길', '28': '놀', '32': '잠', '38': '장', '39': '맛' }

async function load() {
  try {
    const [typeResponse, tourism, food, lodging, postResponse] = await Promise.all([
      contentApi.types(),
      contentApi.list({ contentTypeId: '12', hasImage: true, page: 1, size: 4 }),
      contentApi.list({ contentTypeId: '39', hasImage: true, page: 1, size: 4 }),
      contentApi.list({ contentTypeId: '32', hasImage: true, page: 1, size: 4 }),
      postApi.list({ page: 1, size: 5 }),
    ])
    types.value = typeResponse.items
    featured.value = { tourism: tourism.items, food: food.items, lodging: lodging.items }
    posts.value = postResponse.items
  } catch {
    // 초기 데이터가 없는 경우에도 화면 구조는 유지
  }
}

function search() {
  router.push({ path: '/explore', query: keyword.value ? { keyword: keyword.value } : {} })
}

onMounted(load)
</script>

<template>
  <div>
    <section class="hero">
      <div class="container hero-inner">
        <p class="eyebrow">Gwangju & Jeolla Travel</p>
        <h1>남도의 오늘을<br />한 번에 발견하세요</h1>
        <p>관광지부터 음식점, 숙박, 여행 이야기까지 신뢰할 수 있는 공공데이터로 찾아보세요.</p>
        <form class="hero-search" @submit.prevent="search">
          <input v-model.trim="keyword" placeholder="어디로 떠나고 싶으세요?" aria-label="통합 검색" />
          <button type="submit">검색</button>
        </form>
        <div class="hero-links">
          <button @click="router.push('/explore?areaCode=5')">광주</button>
          <button @click="router.push('/explore?areaCode=37&sigunguCode=12')">전주</button>
          <button @click="router.push('/explore?areaCode=38&sigunguCode=13')">여수</button>
          <button @click="router.push('/explore?areaCode=38&sigunguCode=7')">담양</button>
        </div>
      </div>
    </section>

    <section class="section container">
      <div class="section-heading"><div><p class="eyebrow">Explore by type</p><h2>원하는 여행 방식으로 탐색</h2></div></div>
      <div class="stat-grid">
        <RouterLink v-for="type in types" :key="type.id" :to="`/explore?contentTypeId=${type.id}`" class="stat-card">
          <span>{{ typeIcons[type.id] || '여' }}</span>
          <strong>{{ type.name }}</strong>
          <small>{{ type.count.toLocaleString() }}곳</small>
          <div class="stat-bar"><i :style="{ width: `${Math.max(12, type.count / 5.05)}%` }" /></div>
        </RouterLink>
      </div>
    </section>

    <section class="section section-muted">
      <div class="container">
        <div class="section-heading"><div><p class="eyebrow">Recommended places</p><h2>대표 관광지</h2></div><RouterLink to="/explore?contentTypeId=12">전체 보기 →</RouterLink></div>
        <ContentList :items="featured.tourism" />
      </div>
    </section>

    <section class="section container">
      <div class="section-heading"><div><p class="eyebrow">Taste of Namdo</p><h2>남도의 맛</h2></div><RouterLink to="/explore?contentTypeId=39">음식점 보기 →</RouterLink></div>
      <ContentList :items="featured.food" />
    </section>

    <section class="section section-muted">
      <div class="container">
        <div class="section-heading"><div><p class="eyebrow">Stay</p><h2>여행의 쉼표</h2></div><RouterLink to="/explore?contentTypeId=32">숙박 보기 →</RouterLink></div>
        <ContentList :items="featured.lodging" />
      </div>
    </section>

    <section class="section container community-preview">
      <div class="section-heading"><div><p class="eyebrow">Travel community</p><h2>여행자들의 최신 이야기</h2></div><RouterLink to="/community">커뮤니티 가기 →</RouterLink></div>
      <div class="post-preview-list">
        <RouterLink v-for="post in posts" :key="post.id" :to="`/community/${post.id}`">
          <span>{{ post.category }}</span><strong>{{ post.title }}</strong><small>조회 {{ post.viewCount }}</small>
        </RouterLink>
        <p v-if="!posts.length" class="empty-inline">아직 작성된 글이 없습니다.</p>
      </div>
    </section>
  </div>
</template>
