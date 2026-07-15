<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { postApi } from '../api/postApi'
import PostForm from '../components/community/PostForm.vue'

const router = useRouter()
const error = ref('')

async function submit(payload) {
  try {
    const post = await postApi.create(payload)
    router.push(`/community/${post.id}`)
  } catch (submitError) {
    error.value = submitError.message
  }
}
</script>

<template>
  <section class="form-page section">
    <div class="container form-page-grid">
      <aside class="form-page-intro">
        <span class="section-label">새 여행 이야기</span>
        <h1>궁금한 여행 정보나<br />경험을 편하게 나눠주세요.</h1>
        <p>
          게시글은 익명으로 등록됩니다. 작성 시 설정한 비밀번호는 수정과 삭제에 필요합니다.
        </p>
        <ul>
          <li>카테고리를 알맞게 선택해 주세요.</li>
          <li>구체적인 지역과 상황을 적으면 답변에 도움이 됩니다.</li>
          <li>개인정보와 민감한 정보는 작성하지 마세요.</li>
        </ul>
      </aside>

      <div class="form-card">
        <h2>게시글 작성</h2>
        <p v-if="error" class="error-text" role="alert">{{ error }}</p>
        <PostForm @submit="submit" />
      </div>
    </div>
  </section>
</template>
