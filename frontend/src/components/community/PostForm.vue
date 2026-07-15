<script setup>
import { reactive, watch } from 'vue'

const props = defineProps({
  initialValue: {
    type: Object,
    default: () => ({}),
  },
  submitLabel: {
    type: String,
    default: '등록하기',
  },
})

const emit = defineEmits(['submit'])
const form = reactive({
  category: 'FREE',
  title: '',
  content: '',
  password: '',
  ...props.initialValue,
})

watch(
  () => props.initialValue,
  (value) => Object.assign(form, value),
  { deep: true },
)
</script>

<template>
  <form class="post-form" @submit.prevent="emit('submit', { ...form })">
    <div class="form-row">
      <label class="field-group">
        <span>카테고리</span>
        <select v-model="form.category" :disabled="Boolean(initialValue.category)">
          <option value="TOURISM">관광지</option>
          <option value="FOOD">음식점·맛집</option>
          <option value="LODGING">숙박</option>
          <option value="FESTIVAL">축제·공연</option>
          <option value="COURSE">여행코스</option>
          <option value="FREE">자유</option>
        </select>
      </label>

      <label class="field-group">
        <span>수정·삭제 비밀번호</span>
        <input
          v-model="form.password"
          type="password"
          minlength="4"
          maxlength="30"
          required
          autocomplete="new-password"
          placeholder="4~30자로 입력하세요"
        />
        <small>작성 후 수정하거나 삭제할 때 사용합니다.</small>
      </label>
    </div>

    <label class="field-group">
      <span>제목</span>
      <input
        v-model.trim="form.title"
        minlength="2"
        maxlength="100"
        required
        placeholder="여행자들이 이해하기 쉬운 제목을 입력하세요"
      />
      <small>{{ form.title.length }} / 100</small>
    </label>

    <label class="field-group">
      <span>내용</span>
      <textarea
        v-model.trim="form.content"
        rows="12"
        maxlength="5000"
        required
        placeholder="궁금한 점이나 여행 경험을 자유롭게 적어주세요."
      />
      <small>{{ form.content.length }} / 5,000</small>
    </label>

    <div class="form-notice">
      <span aria-hidden="true">i</span>
      <p>이 게시글은 익명으로 등록됩니다. 개인정보나 민감한 정보는 작성하지 마세요.</p>
    </div>

    <div class="form-actions">
      <RouterLink to="/community" class="button secondary">취소</RouterLink>
      <button class="button primary" type="submit">{{ submitLabel }}</button>
    </div>
  </form>
</template>
