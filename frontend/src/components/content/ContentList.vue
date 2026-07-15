<script setup>
import ContentCard from './ContentCard.vue'
defineProps({ items: { type: Array, default: () => [] } })
</script>

<template>
  <div v-if="items.length" class="content-grid">
    <ContentCard v-for="item in items" :key="item.contentId" :item="item" />
  </div>
  <div v-else class="empty-state">
    <strong>검색 결과가 없습니다.</strong>
    <p>다른 지역이나 검색어로 다시 찾아보세요.</p>
  </div>
</template>
