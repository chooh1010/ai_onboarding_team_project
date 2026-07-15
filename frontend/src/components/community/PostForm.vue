<script setup>
import { reactive, watch } from 'vue'

const props = defineProps({ initialValue: { type: Object, default: () => ({}) }, submitLabel: { type: String, default: '등록하기' } })
const emit = defineEmits(['submit'])
const form = reactive({ category: 'FREE', title: '', content: '', password: '', ...props.initialValue })
watch(() => props.initialValue, (value) => Object.assign(form, value), { deep: true })
</script>

<template>
  <form class="post-form" @submit.prevent="emit('submit', { ...form })">
    <label>
      카테고리
      <select v-model="form.category" :disabled="Boolean(initialValue.category)">
        <option value="TOURISM">관광지</option>
        <option value="FOOD">음식점·맛집</option>
        <option value="LODGING">숙박</option>
        <option value="FESTIVAL">축제·공연</option>
        <option value="COURSE">여행코스</option>
        <option value="FREE">자유</option>
      </select>
    </label>
    <label>
      제목
      <input v-model.trim="form.title" minlength="2" maxlength="100" required />
    </label>
    <label>
      내용
      <textarea v-model.trim="form.content" rows="12" maxlength="5000" required />
    </label>
    <label>
      수정·삭제 비밀번호
      <input v-model="form.password" type="password" minlength="4" maxlength="30" required autocomplete="new-password" />
    </label>
    <button class="button primary" type="submit">{{ submitLabel }}</button>
  </form>
</template>
