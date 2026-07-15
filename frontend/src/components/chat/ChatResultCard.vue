<script setup>
import { resolveImageUrl } from '../../api/http'
defineProps({ result: { type: Object, required: true } })
</script>

<template>
  <RouterLink v-if="result.contentId" :to="`/contents/${result.contentId}`" class="chat-result-card">
    <img v-if="result.imageUrl" :src="resolveImageUrl(result.imageUrl)" alt="" />
    <div>
      <small>{{ result.type }}</small>
      <strong>{{ result.title }}</strong>
      <span>{{ result.address }}</span>
    </div>
  </RouterLink>
  <RouterLink v-else-if="result.postId" :to="`/community/${result.postId}`" class="chat-result-card text-only">
    <div><small>{{ result.type }}</small><strong>{{ result.title }}</strong></div>
  </RouterLink>
</template>
