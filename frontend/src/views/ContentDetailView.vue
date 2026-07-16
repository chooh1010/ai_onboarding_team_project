<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { contentApi } from '../api/contentApi'
import { resolveImageUrl } from '../api/http'
import { getAreaLabel } from '../utils/area'
import ContentList from '../components/content/ContentList.vue'

const route = useRoute()
const item = ref(null)
const nearby = ref([])
const loading = ref(true)
const error = ref('')
const failed = ref(false)

function formatTourDate(value) {
  if (!/^\d{8}$/.test(value || '')) return ''
  const year = Number(value.slice(0, 4))
  const month = Number(value.slice(4, 6))
  const day = Number(value.slice(6, 8))
  return `${year}년 ${month}월 ${day}일`
}

const eventPeriod = computed(() => {
  const start = formatTourDate(item.value?.eventStartDate)
  const end = formatTourDate(item.value?.eventEndDate)
  if (!start) return ''
  if (!end || start === end) return start
  return `${start} ~ ${end}`
})

const image = computed(() => (
  failed.value
    ? ''
    : resolveImageUrl(item.value?.firstImage || item.value?.firstImage2)
))
// 카카오 지도 링크로 변경
const mapLink = computed(() => {
  if (!item.value) return '#'
  const lat = item.value.latitude
  const lng = item.value.longitude
  const title = encodeURIComponent(item.value.title || '장소')
  return `https://map.kakao.com/link/map/${title},${lat},${lng}`
})
const areaLabel = computed(() => getAreaLabel(
  item.value?.areaCode,
  item.value?.sigunguCode,
  item.value?.addr1,
))
const fullAddress = computed(() => (
  [item.value?.addr1, item.value?.addr2].filter(Boolean).join(' ') || '주소 정보 없음'
))
const nearbyLink = computed(() => {
  if (!item.value) return '/explore'
  const query = new URLSearchParams({ areaCode: item.value.areaCode })
  if (item.value.sigunguCode) query.set('sigunguCode', item.value.sigunguCode)
  return `/explore?${query.toString()}`
})

async function load() {
  loading.value = true
  error.value = ''

  try {
    item.value = await contentApi.detail(route.params.contentId)

    try {
      const results = await contentApi.nearby({
        latitude: item.value.latitude,
        longitude: item.value.longitude,
        areaCode: item.value.areaCode,
        radiusKm: 8,
        limit: 5,
      })
      nearby.value = results
        .filter((content) => content.contentId !== item.value.contentId)
        .slice(0, 4)
    } catch (nearbyError) {
      console.error('주변 장소를 불러오지 못했습니다.', nearbyError)
      nearby.value = []
    }
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<template>
  <section v-if="loading" class="section container detail-loading">
    <span />
    <strong>장소 정보를 불러오는 중입니다.</strong>
  </section>

  <section v-else-if="error" class="section container">
    <div class="error-panel" role="alert">
      <strong>장소 정보를 불러오지 못했습니다.</strong>
      <p>{{ error }}</p>
      <RouterLink to="/explore" class="button secondary">여행지 목록으로</RouterLink>
    </div>
  </section>

  <template v-else-if="item">
    <section class="detail-hero">
      <div class="container detail-topbar">
        <RouterLink to="/explore" class="back-link">
          <span aria-hidden="true">←</span> 여행지 목록
        </RouterLink>
        <span>{{ areaLabel }} · {{ item.contentTypeName }}</span>
      </div>

      <div class="container detail-hero-grid">
        <div class="detail-image">
          <img
            v-if="image"
            :src="image"
            :alt="`${item.title} 대표 이미지`"
            @error="failed = true"
          />
          <div v-else class="image-fallback large" aria-label="대표 이미지 없음">
            <span class="fallback-sun" />
            <span class="fallback-hill fallback-hill-back" />
            <span class="fallback-hill fallback-hill-front" />
            <strong>대표 이미지가 제공되지 않았어요.</strong>
          </div>
        </div>

        <div class="detail-heading">
          <span class="type-badge static">{{ item.contentTypeName }}</span>
          <p class="detail-region">{{ areaLabel }}</p>
          <h1>{{ item.title }}</h1>
          <p class="detail-address">{{ fullAddress }}</p>

          <div class="detail-actions">
            <a
              class="button primary"
              :href="mapLink"
              target="_blank"
              rel="noreferrer"
            >
              지도에서 위치 보기 <span aria-hidden="true">↗</span>
            </a>
            <RouterLink :to="nearbyLink" class="button secondary">
              주변 장소 탐색 <span aria-hidden="true">→</span>
            </RouterLink>
          </div>

          <p class="detail-origin-note">
            <span aria-hidden="true">i</span>
            원본 관광정보의 주소와 이미지를 임의로 수정하지 않았습니다.
          </p>
        </div>
      </div>
    </section>

    <section class="section detail-content-section">
      <div class="container detail-content-grid">
        <article class="detail-info-card">
          <div class="detail-card-heading">
            <span class="section-label">장소 정보</span>
            <h2>방문 전에 확인하세요.</h2>
          </div>

          <dl class="detail-list">
            <div>
              <dt>주소</dt>
              <dd>{{ fullAddress }}</dd>
            </div>
            <div v-if="eventPeriod">
              <dt>행사 기간</dt>
              <dd>{{ eventPeriod }}</dd>
            </div>
            <div v-if="item.eventPlace">
              <dt>행사 장소</dt>
              <dd>{{ item.eventPlace }}</dd>
            </div>
            <div v-if="item.playtime">
              <dt>행사 시간</dt>
              <dd>{{ item.playtime }}</dd>
            </div>
            <div v-if="item.program">
              <dt>프로그램</dt>
              <dd>{{ item.program }}</dd>
            </div>
            <div v-if="item.subevent">
              <dt>부대 행사</dt>
              <dd>{{ item.subevent }}</dd>
            </div>
            <div v-if="item.useTimeFestival">
              <dt>이용 요금</dt>
              <dd>{{ item.useTimeFestival }}</dd>
            </div>
            <div v-if="item.ageLimit">
              <dt>관람 연령</dt>
              <dd>{{ item.ageLimit }}</dd>
            </div>
            <div v-if="item.bookingPlace">
              <dt>예매처</dt>
              <dd>{{ item.bookingPlace }}</dd>
            </div>
            <div v-if="item.eventHomepage">
              <dt>행사 홈페이지</dt>
              <dd>{{ item.eventHomepage }}</dd>
            </div>
            <div v-if="item.tel">
              <dt>전화번호</dt>
              <dd>{{ item.tel }}</dd>
            </div>
            <div v-if="item.zipcode">
              <dt>우편번호</dt>
              <dd>{{ item.zipcode }}</dd>
            </div>
            <div>
              <dt>좌표</dt>
              <dd>{{ item.latitude }}, {{ item.longitude }}</dd>
            </div>
            <div>
              <dt>콘텐츠 ID</dt>
              <dd>{{ item.contentId }}</dd>
            </div>
          </dl>
        </article>

        <aside class="detail-source-card">
          <span class="source-seal" aria-hidden="true">公</span>
          <span class="section-label">데이터 출처</span>
          <h2>공공데이터를 바탕으로 안내합니다.</h2>
          <dl>
            <div>
              <dt>제공 기관</dt>
              <dd>{{ item.source.provider }}</dd>
            </div>
            <div>
              <dt>라이선스</dt>
              <dd>{{ item.source.license }}</dd>
            </div>
            <div>
              <dt>원본 변경</dt>
              <dd>금지</dd>
            </div>
          </dl>
          <RouterLink to="/data-source" class="text-link">
            데이터 범위와 한계 확인 <span aria-hidden="true">→</span>
          </RouterLink>
        </aside>
      </div>
    </section>

    <section v-if="nearby.length" class="section nearby-section">
      <div class="container">
        <div class="section-heading">
          <div>
            <span class="section-label">가까운 장소</span>
            <h2>이곳과 함께 둘러볼 만한 곳</h2>
          </div>
          <RouterLink :to="nearbyLink" class="text-link">
            같은 지역 더 보기 <span aria-hidden="true">→</span>
          </RouterLink>
        </div>
        <ContentList :items="nearby" />
      </div>
    </section>
  </template>
</template>
