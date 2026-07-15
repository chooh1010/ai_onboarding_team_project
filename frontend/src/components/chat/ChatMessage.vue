<script setup>
import ChatResultCard from './ChatResultCard.vue'
defineProps({ message: { type: Object, required: true } })
</script>

<template>
  <div :class="['chat-message', message.role]">
    <div class="bubble">{{ message.content }}</div>
    <div v-if="message.results?.length" class="chat-results">
      <ChatResultCard v-for="(result, index) in message.results" :key="result.contentId || result.postId || index" :result="result" />
    </div>
  </div>
</template>
