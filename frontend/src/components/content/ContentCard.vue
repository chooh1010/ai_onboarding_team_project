<script setup>
import { computed, ref } from 'vue'
import { resolveImageUrl } from '../../api/http'
import { getAreaLabel } from '../../utils/area'

const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
})

const failed = ref(false)

function formatTourDate(value) {
  if (!/^\d{8}$/.test(value || '')) return ''
  return `${Number(value.slice(4, 6))}월 ${Number(value.slice(6, 8))}일`
}

const eventPeriod = computed(() => {
  const start = formatTourDate(props.item.eventStartDate)
  const end = formatTourDate(props.item.eventEndDate)
  if (!start) return ''
  if (!end || start === end) return start
  return `${start} ~ ${end}`
})

const image = computed(() => (
  failed.value
    ? ''
    : resolveImageUrl(props.item.thumbnailUrl || props.item.firstImage)
))
const areaLabel = computed(() => getAreaLabel(
  props.item.areaCode,
  props.item.sigunguCode,
  props.item.address,
))
</script>

<template>
  <article class="content-card">
    <RouterLink :to="`/contents/${item.contentId}`" class="card-image-wrap">
      <img
        v-if="image"
        :src="image"
        :alt="`${item.title} 대표 이미지`"
        class="card-image"
        loading="lazy"
        @error="failed = true"
      />
      <div v-else class="image-fallback" aria-label="대표 이미지 없음">
        <span class="fallback-sun" />
        <span class="fallback-hill fallback-hill-back" />
        <span class="fallback-hill fallback-hill-front" />
        <strong>남도의 풍경을<br />준비하고 있어요</strong>
      </div>
      <span class="type-badge">{{ item.contentTypeName }}</span>
      <span class="area-badge">{{ areaLabel }}</span>
    </RouterLink>

    <div class="card-body">
      <div>
        <p class="card-kicker">{{ areaLabel }} · {{ item.contentTypeName }}</p>
        <h3>
          <RouterLink :to="`/contents/${item.contentId}`">
            {{ item.title }}
          </RouterLink>
        </h3>
        <p v-if="eventPeriod" class="card-address">행사 기간 · {{ eventPeriod }}</p>
        <p class="card-address">{{ item.address || '주소 정보가 제공되지 않았습니다.' }}</p>
      </div>

      <div class="card-meta">
        <span v-if="item.distanceKm !== null && item.distanceKm !== undefined" class="distance-chip">
          현재 위치에서 {{ item.distanceKm }}km
        </span>
        <RouterLink :to="`/contents/${item.contentId}`" class="card-link">
          상세 보기 <span aria-hidden="true">→</span>
        </RouterLink>
      </div>
    </div>
  </article>
</template>
