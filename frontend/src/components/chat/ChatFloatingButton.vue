<script setup>
import { ref } from 'vue'
import ChatWindow from './ChatWindow.vue'
const open = ref(false)
</script>

<template>
  <div class="chat-floating">
    <ChatWindow v-if="open" @close="open = false" />
    <button class="chat-toggle" :aria-expanded="open" aria-label="관광 안내 챗봇 열기" @click="open = !open">
      {{ open ? '×' : '여행톡' }}
    </button>
  </div>
</template>
