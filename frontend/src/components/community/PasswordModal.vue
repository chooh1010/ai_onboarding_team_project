<script setup>
import { ref } from 'vue'

defineProps({
  title: {
    type: String,
    default: '비밀번호 확인',
  },
})

const emit = defineEmits(['close', 'confirm'])
const password = ref('')
</script>

<template>
  <div class="modal-backdrop" @click.self="emit('close')">
    <section class="modal-card" role="dialog" aria-modal="true" aria-labelledby="password-modal-title">
      <button class="modal-close" type="button" aria-label="창 닫기" @click="emit('close')">×</button>
      <span class="modal-icon" aria-hidden="true">鍵</span>
      <h2 id="password-modal-title">{{ title }}</h2>
      <p>게시글을 작성할 때 설정한 비밀번호를 입력해 주세요.</p>
      <label class="field-group">
        <span>비밀번호</span>
        <input
          v-model="password"
          type="password"
          minlength="4"
          maxlength="30"
          autofocus
          placeholder="비밀번호 입력"
          @keyup.enter="emit('confirm', password)"
        />
      </label>
      <div class="modal-actions">
        <button class="button secondary" type="button" @click="emit('close')">취소</button>
        <button class="button danger" type="button" @click="emit('confirm', password)">확인</button>
      </div>
    </section>
  </div>
</template>
