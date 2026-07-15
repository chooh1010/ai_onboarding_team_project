<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { postApi } from '../api/postApi'
import PostForm from '../components/community/PostForm.vue'

const route = useRoute()
const router = useRouter()
const post = ref(null)
const error = ref('')

onMounted(async () => {
  try {
    post.value = await postApi.detail(route.params.postId)
  } catch (loadError) {
    error.value = loadError.message
  }
})

async function submit(payload) {
  try {
    const updated = await postApi.update(route.params.postId, payload)
    router.push(`/community/${updated.id}`)
  } catch (submitError) {
    error.value = submitError.message
  }
}
</script>

<template>
  <section class="form-page section">
    <div class="container form-page-grid">
      <aside class="form-page-intro">
        <span class="section-label">여행 이야기 수정</span>
        <h1>작성한 내용을<br />다시 다듬어보세요.</h1>
        <p>게시글 작성 시 설정한 비밀번호가 일치해야 수정할 수 있습니다.</p>
      </aside>

      <div v-if="post" class="form-card">
        <h2>게시글 수정</h2>
        <p v-if="error" class="error-text" role="alert">{{ error }}</p>
        <PostForm
          :initial-value="{
            category: post.category,
            title: post.title,
            content: post.content,
          }"
          submit-label="수정 완료"
          @submit="submit"
        />
      </div>

      <div v-else-if="error" class="error-panel" role="alert">
        <strong>게시글을 불러오지 못했습니다.</strong>
        <p>{{ error }}</p>
        <RouterLink to="/community" class="button secondary">목록으로</RouterLink>
      </div>

      <div v-else class="content-loading">
        <span />
        <strong>게시글을 불러오는 중입니다.</strong>
      </div>
    </div>
  </section>
</template>
