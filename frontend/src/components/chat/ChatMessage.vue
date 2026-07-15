<script setup>
import ChatResultCard from './ChatResultCard.vue'

defineProps({
  message: {
    type: Object,
    required: true,
  },
})
</script>

<template>
  <div :class="['chat-message', message.role, { error: message.error }]">
    <span v-if="message.role === 'assistant'" class="message-avatar" aria-hidden="true">旅</span>
    <div class="message-content">
      <div class="bubble">{{ message.content }}</div>
      <div v-if="message.results?.length" class="chat-results">
        <ChatResultCard
          v-for="(result, index) in message.results"
          :key="result.contentId || result.postId || index"
          :result="result"
        />
      </div>
      <div v-if="message.limitations?.length" class="chat-limitations">
        <strong>확인하기 어려운 정보</strong>
        <span v-for="limitation in message.limitations" :key="limitation">{{ limitation }}</span>
      </div>
    </div>
  </div>
</template>
