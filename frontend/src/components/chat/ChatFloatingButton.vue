<script setup>
import { ref } from 'vue'
import ChatWindow from './ChatWindow.vue'
import WeatherMap from '../WeatherMap.vue'

const open = ref(false)
const weatherOpen = ref(false)
</script>

<template>
  <div class="chat-floating">
    <div v-if="weatherOpen" class="weather-floating-panel">
      <WeatherMap />
    </div>

    <ChatWindow v-if="open" @close="open = false" />

    <button
      class="chat-toggle"
      type="button"
      :aria-expanded="weatherOpen"
      aria-label="날씨 보기"
      @click="weatherOpen = !weatherOpen"
    >
      <span class="chat-toggle-symbol" aria-hidden="true">{{ weatherOpen ? '×' : '天' }}</span>
      <span v-if="!weatherOpen" class="chat-toggle-copy">
        <strong>날씨</strong>
        <small>광주 권역 현재</small>
      </span>
    </button>

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

<style scoped>
.weather-floating-panel {
  margin-bottom: 8px;
}
</style>