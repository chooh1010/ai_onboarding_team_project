<script setup>
import { ref } from 'vue'
defineProps({ title: { type: String, default: '비밀번호 확인' } })
const emit = defineEmits(['close', 'confirm'])
const password = ref('')
</script>

<template>
  <div class="modal-backdrop" @click.self="emit('close')">
    <section class="modal-card" role="dialog" aria-modal="true">
      <h2>{{ title }}</h2>
      <p>게시글 작성 시 설정한 비밀번호를 입력하세요.</p>
      <input v-model="password" type="password" minlength="4" maxlength="30" autofocus @keyup.enter="emit('confirm', password)" />
      <div class="modal-actions">
        <button class="button ghost" @click="emit('close')">취소</button>
        <button class="button danger" @click="emit('confirm', password)">확인</button>
      </div>
    </section>
  </div>
</template>
