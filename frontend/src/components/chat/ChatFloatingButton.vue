<script setup>
import { ref } from 'vue'
import ChatWindow from './ChatWindow.vue'

const open = ref(false)
</script>

<template>
  <div class="chat-floating">
    <ChatWindow v-if="open" @close="open = false" />

    <button
      class="chat-toggle"
      type="button"
      :aria-expanded="open"
      aria-label="관광 안내 챗봇 열기"
      @click="open = !open"
    >
      <span class="chat-toggle-symbol" aria-hidden="true">{{ open ? '×' : '旅' }}</span>
      <span v-if="!open" class="chat-toggle-copy">
        <strong>남도 여행톡</strong>
        <small>무엇을 찾고 있나요?</small>
      </span>
    </button>
  </div>
</template>
