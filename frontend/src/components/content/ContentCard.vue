<script setup>
import { computed, ref } from 'vue'
import { resolveImageUrl } from '../../api/http'

const props = defineProps({ item: { type: Object, required: true } })
const failed = ref(false)
const image = computed(() => failed.value ? '' : resolveImageUrl(props.item.thumbnailUrl || props.item.firstImage))
</script>

<template>
  <article class="content-card">
    <RouterLink :to="`/contents/${item.contentId}`" class="card-image-wrap">
      <img v-if="image" :src="image" :alt="`${item.title} 대표 이미지`" class="card-image" @error="failed = true" />
      <div v-else class="image-fallback" aria-label="대표 이미지 없음">
        <span>남도온</span>
        <small>이미지 준비 중</small>
      </div>
      <span class="type-badge">{{ item.contentTypeName }}</span>
    </RouterLink>
    <div class="card-body">
      <h3><RouterLink :to="`/contents/${item.contentId}`">{{ item.title }}</RouterLink></h3>
      <p>{{ item.address || '주소 정보 없음' }}</p>
      <div class="card-meta">
        <span v-if="item.distanceKm !== null && item.distanceKm !== undefined">{{ item.distanceKm }}km</span>
        <RouterLink :to="`/contents/${item.contentId}`">상세 보기 →</RouterLink>
      </div>
    </div>
  </article>
</template>
