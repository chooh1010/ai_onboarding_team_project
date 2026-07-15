<script setup>
import ContentCard from './ContentCard.vue'

defineProps({
  items: {
    type: Array,
    default: () => [],
  },
})
</script>

<template>
  <div v-if="items.length" class="content-grid">
    <ContentCard
      v-for="item in items"
      :key="item.contentId"
      :item="item"
    />
  </div>

  <div v-else class="empty-state">
    <span class="empty-state-icon" aria-hidden="true">⌕</span>
    <strong>조건에 맞는 장소를 찾지 못했어요.</strong>
    <p>지역을 넓히거나 다른 검색어로 다시 찾아보세요.</p>
    <RouterLink to="/explore" class="button secondary">전체 장소 보기</RouterLink>
  </div>
</template>
