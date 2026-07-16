<script setup>
import { computed, onMounted, ref } from 'vue'
import WeatherMap from '../components/WeatherMap.vue'
import { useRouter } from 'vue-router'
import { contentApi } from '../api/contentApi'
import { postApi } from '../api/postApi'
import { resolveImageUrl } from '../api/http'
import ContentList from '../components/content/ContentList.vue'
import { applySpacing } from '../utils/spacing'

const router = useRouter()
const keyword = ref('')
const types = ref([])
const featured = ref({ tourism: [], food: [], lodging: [] })
const posts = ref([])
const heroImageFailed = ref(false)

const fallbackTypes = [
  { id: '12', name: '관광지', count: 505 },
  { id: '39', name: '음식점', count: 416 },
  { id: '32', name: '숙박', count: 191 },
  { id: '14', name: '문화시설', count: 86 },
  { id: '28', name: '레포츠', count: 85 },
  { id: '25', name: '여행코스', count: 55 },
  { id: '38', name: '쇼핑', count: 38 },
  { id: '15', name: '축제·행사', count: 17 },
]

const typeMeta = {
  '12': { icon: '山', copy: '자연과 명소' },
  '14': { icon: '文', copy: '전시와 문화' },
  '15': { icon: '樂', copy: '축제와 공연' },
  '25': { icon: '路', copy: '여행의 흐름' },
  '28': { icon: '動', copy: '활동과 체험' },
  '32': { icon: '宿', copy: '편안한 머묾' },
  '38': { icon: '品', copy: '지역의 물건' },
  '39': { icon: '味', copy: '남도의 맛' },
}

const regionLinks = [
  { name: '광주', description: '도시와 예술', query: { areaCode: '5' } },
  { name: '전주', description: '한옥과 전통', query: { areaCode: '37', sigunguCode: '12' } },
  { name: '여수', description: '바다와 야경', query: { areaCode: '38', sigunguCode: '13' } },
  { name: '담양', description: '대숲과 쉼', query: { areaCode: '38', sigunguCode: '7' } },
  { name: '순천', description: '정원과 생태', query: { areaCode: '38', sigunguCode: '11' } },
  { name: '남원', description: '문화와 산책', query: { areaCode: '37', sigunguCode: '4' } },
]

const displayTypes = computed(() => (types.value.length ? types.value : fallbackTypes))
const totalCount = computed(() => displayTypes.value.reduce(
  (sum, type) => sum + Number(type.count || 0),
  0,
))
const heroPlace = computed(() => featured.value.tourism[0] || null)
const heroImage = computed(() => {
  if (heroImageFailed.value) return ''
  return resolveImageUrl(
    heroPlace.value?.thumbnailUrl
      || heroPlace.value?.firstImage
      || '',
  )
})

const categoryLabels = {
  TOURISM: '관광지',
  FOOD: '음식점·맛집',
  LODGING: '숙박',
  FESTIVAL: '축제·공연',
  COURSE: '여행코스',
  FREE: '자유',
}

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
    featured.value = {
      tourism: tourism.items,
      food: food.items,
      lodging: lodging.items,
    }
    posts.value = postResponse.items.map(p => ({
      ...p,
      title: applySpacing(p.title),
      // 필요하면 summary/contents도 적용
      // summary: applySpacing(p.summary)
    }));

    // featured 값 설정 예시 (각 아이템의 title 보정)
    featured.value = {
      tourism: tourism.items.map(i => ({ ...i, title: applySpacing(i.title) })),
      food:    food.items.map(i => ({ ...i, title: applySpacing(i.title) })),
      lodging: lodging.items.map(i => ({ ...i, title: applySpacing(i.title) })),
    };
  } catch (error) {
    console.error('홈 화면 데이터를 불러오지 못했습니다.', error)
  }
}

function search() {
  router.push({
    path: '/explore',
    query: keyword.value ? { keyword: keyword.value } : {},
  })
}

function moveToRegion(query) {
  router.push({ path: '/explore', query })
}

onMounted(load)
</script>

<template>
  <div class="home-page">
    <section class="home-hero">
      <div class="hero-media" aria-hidden="true">
        <img
          v-if="heroImage"
          :src="heroImage"
          alt=""
          @error="heroImageFailed = true"
        />
        <div v-else class="hero-media-fallback">
          <span class="scenery-sun" />
          <span class="scenery-mountain scenery-mountain-back" />
          <span class="scenery-mountain scenery-mountain-front" />
        </div>
      </div>

      <div class="hero-overlay" />

      <div class="container home-hero-inner">
        <div class="hero-copy">
          <p class="hero-eyebrow">
            <span aria-hidden="true">●</span>
            광주·전라권 관광정보 {{ totalCount.toLocaleString() }}곳
          </p>
          <h1>
            천천히 머물고 싶은<br />
            <em>남도의 오늘</em>을 만나보세요.
          </h1>
          <p class="hero-description">
            자연, 음식, 문화와 머물 곳까지 한 번에 살펴보고<br class="desktop-only" />
            나에게 맞는 광주·전라 여행을 시작하세요.
          </p>

          <form class="hero-search" @submit.prevent="search">
            <span class="hero-search-icon" aria-hidden="true">⌕</span>
            <label>
              <span>어디를 찾고 계세요?</span>
              <input
                v-model.trim="keyword"
                aria-label="관광정보 통합 검색"
                placeholder="예: 여수 바다, 담양 관광지, 전주 숙박"
              />
            </label>
            <button type="submit">
              검색하기 <span aria-hidden="true">→</span>
            </button>
          </form>

          <div class="hero-region-links" aria-label="인기 지역 바로가기">
            <span>추천 지역</span>
            <button
              v-for="region in regionLinks.slice(0, 4)"
              :key="region.name"
              type="button"
              @click="moveToRegion(region.query)"
            >
              {{ region.name }}
            </button>
          </div>
        </div>

        <aside class="hero-place-note">
          <span class="hero-place-number">오늘의 남도</span>
          <strong>{{ heroPlace?.title || '광주·전라의 아름다운 풍경' }}</strong>
          <p>{{ heroPlace?.address || '지역의 자연과 문화를 천천히 둘러보세요.' }}</p>

          <RouterLink v-if="heroPlace" :to="`/contents/${heroPlace.contentId}`">
            이 장소 자세히 보기 <span aria-hidden="true">→</span>
          </RouterLink>
          <RouterLink v-else to="/explore">
            여행지 둘러보기 <span aria-hidden="true">→</span>
          </RouterLink>
        </aside>
      </div>

      <div class="container hero-summary" aria-label="서비스 데이터 요약">
        <div>
          <strong>{{ totalCount.toLocaleString() }}</strong>
          <span>등록 관광 콘텐츠</span>
        </div>
        <div>
          <strong>8</strong>
          <span>관광 콘텐츠 유형</span>
        </div>
        <div>
          <strong>11</strong>
          <span>주요 여행 지역</span>
        </div>
        <div class="hero-source-summary">
          <small>DATA SOURCE</small>
          <span>한국관광공사 TourAPI 4.0</span>
        </div>
      </div>
    </section>

    <!-- Region cards -->
    <section class="section region-section">
      <div class="container">
        <div class="section-heading split-heading">
          <div>
            <span class="section-label">지역으로 떠나기</span>
            <h2>남도의 서로 다른 표정을<br />지역별로 만나보세요.</h2>
          </div>
        </div>

        <div class="region-grid">
          <button
            v-for="(region, index) in regionLinks"
            :key="region.name"
            type="button"
            :class="['region-card', `region-card-${index + 1}`]"
            @click="moveToRegion(region.query)"
          >
            <span class="region-number">0{{ index + 1 }}</span>
            <span class="region-card-copy">
              <strong>{{ region.name }}</strong>
              <small>{{ region.description }}</small>
            </span>
            <span class="region-arrow" aria-hidden="true">↗</span>
          </button>
        </div>
      </div>
    </section>

    <!-- Category / featured lists -->
    <section class="section category-section">
      <div class="container">
        <div class="section-heading">
          <div>
            <span class="section-label">여행 방식으로 찾기</span>
            <h2>오늘의 여행에 필요한 것부터</h2>
          </div>
          <RouterLink to="/explore" class="text-link">
            전체 콘텐츠 보기 <span aria-hidden="true">→</span>
          </RouterLink>
        </div>

        <div class="category-grid">
          <RouterLink
            v-for="type in displayTypes"
            :key="type.id"
            :to="`/explore?contentTypeId=${type.id}`"
            class="category-card"
          >
            <span class="category-icon" aria-hidden="true">
              {{ typeMeta[type.id]?.icon || '旅' }}
            </span>
            <span class="category-card-copy">
              <small>{{ typeMeta[type.id]?.copy || '남도 여행' }}</small>
              <strong>{{ type.name }}</strong>
              <span>{{ Number(type.count).toLocaleString() }}곳</span>
            </span>
            <span class="category-arrow" aria-hidden="true">→</span>
          </RouterLink>
        </div>
      </div>
    </section>

    <section class="section recommendation-section">
      <div class="container">
        <div class="section-heading">
          <div>
            <span class="section-label">추천 관광지</span>
            <h2>풍경을 따라 떠나는 남도 여행</h2>
          </div>
          <RouterLink to="/explore?contentTypeId=12" class="text-link">
            관광지 더 보기 <span aria-hidden="true">→</span>
          </RouterLink>
        </div>
        <ContentList :items="featured.tourism" />
      </div>
    </section>

    <section class="section food-section">
      <div class="container">
        <div class="section-heading light-heading">
          <div>
            <span class="section-label">남도의 맛</span>
            <h2>여행을 오래 기억하게 하는 한 끼</h2>
          </div>
          <RouterLink to="/explore?contentTypeId=39" class="text-link">
            음식점 더 보기 <span aria-hidden="true">→</span>
          </RouterLink>
        </div>
        <ContentList :items="featured.food" />
      </div>
    </section>

    <section class="section recommendation-section">
      <div class="container">
        <div class="section-heading">
          <div>
            <span class="section-label">편안하게 머물다 가기</span>
            <h2>하루를 천천히 마무리할 곳</h2>
          </div>
          <RouterLink to="/explore?contentTypeId=32" class="text-link">
            숙박 더 보기 <span aria-hidden="true">→</span>
          </RouterLink>
        </div>
        <ContentList :items="featured.lodging" />
      </div>
    </section>

    <section class="section community-home-section">
      <div class="container community-home-grid">
        <div class="community-home-intro">
          <span class="section-label">여행자의 이야기</span>
          <h2>정보만으로 부족할 때,<br />먼저 다녀온 사람에게 물어보세요.</h2>
          <p>
            맛집 추천, 숙소 선택, 여행코스 고민까지 익명으로 편하게 묻고
            광주·전라 여행 경험을 나눌 수 있습니다.
          </p>
          <div class="community-home-actions">
            <RouterLink to="/community" class="button primary">커뮤니티 둘러보기</RouterLink>
            <RouterLink to="/community/write" class="button secondary">이야기 남기기</RouterLink>
          </div>
        </div>

        <div class="post-preview-list">
          <RouterLink
            v-for="post in posts"
            :key="post.id"
            :to="`/community/${post.id}`"
          >
            <span class="post-preview-category">{{ categoryLabels[post.category] || post.category }}</span>
            <strong>{{ post.title }}</strong>
            <small>
              {{ new Date(post.createdAt).toLocaleDateString('ko-KR') }} · 조회 {{ post.viewCount }}
            </small>
            <span class="post-preview-arrow" aria-hidden="true">→</span>
          </RouterLink>

          <div v-if="!posts.length" class="post-preview-empty">
            <strong>아직 등록된 여행 이야기가 없어요.</strong>
            <p>첫 번째 질문이나 여행 후기를 남겨보세요.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section source-home-section">
      <div class="container source-home-card">
        <div class="source-home-mark" aria-hidden="true">公</div>
        <div>
          <span class="section-label">믿을 수 있는 여행정보</span>
          <h2>데이터가 말해주는 범위 안에서<br />정확하게 안내합니다.</h2>
          <p>
            한국관광공사 TourAPI 4.0 원본 데이터를 사용하며, 주소와 이미지를 임의로
            변경하지 않습니다. 데이터에 없는 일정, 가격, 영업시간도 추측하지 않습니다.
          </p>
        </div>
        <RouterLink to="/data-source" class="button secondary">
          데이터 출처와 한계 보기 <span aria-hidden="true">→</span>
        </RouterLink>
      </div>
    </section>
  </div>
</template>

<style scoped>
.weather-home-section {
  padding-top: 10px;
  padding-bottom: 10px;
}

.weather-home-slot {
  width: fit-content;
  max-width: 300px;
  margin-left: 0;
  margin-right: auto;
  padding-left: 2px;
}
</style>