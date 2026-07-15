<script setup>
import { computed, ref } from 'vue'
import { resolveImageUrl } from '../../api/http'

const props = defineProps({
  result: {
    type: Object,
    required: true,
  },
})

const failed = ref(false)
const image = computed(() => (
  failed.value ? '' : resolveImageUrl(props.result.imageUrl)
))
</script>

<template>
  <RouterLink
    v-if="result.contentId"
    :to="`/contents/${result.contentId}`"
    class="chat-result-card"
  >
    <div class="chat-result-image">
      <img
        v-if="image"
        :src="image"
        :alt="`${result.title} 이미지`"
        @error="failed = true"
      />
      <span v-else aria-hidden="true">旅</span>
    </div>
    <div>
      <small>{{ result.type }}</small>
      <strong>{{ result.title }}</strong>
      <span>{{ result.address || '주소 정보 없음' }}</span>
    </div>
    <i aria-hidden="true">→</i>
  </RouterLink>

  <RouterLink
    v-else-if="result.postId"
    :to="`/community/${result.postId}`"
    class="chat-result-card text-only"
  >
    <div class="chat-result-image"><span aria-hidden="true">話</span></div>
    <div>
      <small>{{ result.type }}</small>
      <strong>{{ result.title }}</strong>
    </div>
    <i aria-hidden="true">→</i>
  </RouterLink>
</template>
