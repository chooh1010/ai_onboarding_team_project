<script setup>
import { nextTick, ref } from 'vue'
import { chatApi } from '../../api/chatApi'
import ChatMessage from './ChatMessage.vue'

const emit = defineEmits(['close'])
const input = ref('')
const loading = ref(false)
const scroller = ref(null)
const messages = ref([
  {
    role: 'assistant',
    content: '안녕하세요. 광주·전라권 관광정보를 찾아드릴게요. 지역과 원하는 장소 유형을 말씀해 주세요.',
  },
])
const suggestions = [
  '광주 동구 관광지 알려줘',
  '전주에 있는 숙박시설 추천해줘',
  '여수 음식점을 찾아줘',
  '떡갈비 관련 커뮤니티 글 찾아줘',
  '이번 주말 축제 알려줘',
]

async function scrollToBottom(behavior = 'auto') {
  await nextTick()
  scroller.value?.scrollTo({
    top: scroller.value.scrollHeight,
    behavior,
  })
}

async function send(text = input.value) {
  const message = text.trim()
  if (!message || loading.value) return

  messages.value.push({ role: 'user', content: message })
  input.value = ''
  loading.value = true
  await scrollToBottom()

  try {
    const history = messages.value
      .slice(-8, -1)
      .map(({ role, content }) => ({ role, content }))
    const response = await chatApi.send(message, history)
    messages.value.push({
      role: 'assistant',
      content: response.answer,
      results: response.results,
      limitations: response.limitations,
    })
  } catch (error) {
    messages.value.push({
      role: 'assistant',
      content: error.message,
      error: true,
    })
  } finally {
    loading.value = false
    await scrollToBottom('smooth')
  }
}
</script>

<template>
  <section class="chat-window" aria-label="광주·전라권 관광 안내 챗봇">
    <header class="chat-header">
      <div class="chat-agent-mark" aria-hidden="true">旅</div>
      <div>
        <strong>남도 여행톡</strong>
        <small><span /> 제공 데이터 안에서만 안내해요</small>
      </div>
      <button type="button" aria-label="챗봇 닫기" @click="emit('close')">×</button>
    </header>

    <div ref="scroller" class="chat-scroll">
      <div class="chat-welcome">
        <span class="section-label">추천 질문</span>
        <p>아래 질문을 선택하거나 궁금한 내용을 직접 입력해 보세요.</p>
        <div class="suggestions">
          <button
            v-for="suggestion in suggestions"
            :key="suggestion"
            type="button"
            @click="send(suggestion)"
          >
            {{ suggestion }}
          </button>
        </div>
      </div>

      <ChatMessage
        v-for="(message, index) in messages"
        :key="index"
        :message="message"
      />

      <div v-if="loading" class="typing" aria-live="polite">
        <span />
        <span />
        <span />
        관광정보를 찾고 있어요.
      </div>
    </div>

    <form class="chat-form" @submit.prevent="send()">
      <label>
        <span class="sr-only">챗봇 질문</span>
        <input
          v-model="input"
          placeholder="예: 전주 관광지 알려줘"
          aria-label="챗봇 질문"
        />
      </label>
      <button type="submit" :disabled="loading || !input.trim()">
        <span class="sr-only">전송</span>
        <span aria-hidden="true">↑</span>
      </button>
    </form>

    <p class="chat-source-note">출처: 한국관광공사 TourAPI 4.0 · 공공누리 제3유형</p>
  </section>
</template>
