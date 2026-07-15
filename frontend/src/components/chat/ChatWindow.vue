<script setup>
import { nextTick, ref } from 'vue'
import { chatApi } from '../../api/chatApi'
import ChatMessage from './ChatMessage.vue'

const emit = defineEmits(['close'])
const input = ref('')
const loading = ref(false)
const scroller = ref(null)
const messages = ref([
  { role: 'assistant', content: '광주·전라권 여행 정보를 찾아드릴게요. 지역과 원하는 콘텐츠를 말씀해 주세요.' },
])
const suggestions = [
  '광주 동구 관광지 알려줘',
  '전주에 있는 숙박시설 추천해줘',
  '여수 음식점을 찾아줘',
  '떡갈비 관련 커뮤니티 글 찾아줘',
  '이번 주말 축제 알려줘',
]

async function send(text = input.value) {
  const message = text.trim()
  if (!message || loading.value) return
  messages.value.push({ role: 'user', content: message })
  input.value = ''
  loading.value = true
  await nextTick()
  scroller.value?.scrollTo({ top: scroller.value.scrollHeight })
  try {
    const history = messages.value.slice(-8, -1).map(({ role, content }) => ({ role, content }))
    const response = await chatApi.send(message, history)
    messages.value.push({ role: 'assistant', content: response.answer, results: response.results })
  } catch (error) {
    messages.value.push({ role: 'assistant', content: error.message })
  } finally {
    loading.value = false
    await nextTick()
    scroller.value?.scrollTo({ top: scroller.value.scrollHeight, behavior: 'smooth' })
  }
}
</script>

<template>
  <section class="chat-window" aria-label="관광 안내 챗봇">
    <header>
      <div><strong>남도온 여행 도우미</strong><small>제공 데이터 안에서만 답변해요</small></div>
      <button aria-label="챗봇 닫기" @click="emit('close')">×</button>
    </header>
    <div ref="scroller" class="chat-scroll">
      <div class="suggestions">
        <button v-for="suggestion in suggestions" :key="suggestion" @click="send(suggestion)">{{ suggestion }}</button>
      </div>
      <ChatMessage v-for="(message, index) in messages" :key="index" :message="message" />
      <div v-if="loading" class="typing">검색 중…</div>
    </div>
    <form @submit.prevent="send()">
      <input v-model="input" placeholder="예: 전주 관광지 알려줘" aria-label="챗봇 질문" />
      <button type="submit">전송</button>
    </form>
  </section>
</template>
