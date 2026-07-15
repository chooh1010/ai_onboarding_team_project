<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { postApi } from '../api/postApi'
import PasswordModal from '../components/community/PasswordModal.vue'

const route = useRoute()
const router = useRouter()
const post = ref(null)
const modal = ref(false)
const error = ref('')
const loading = ref(true)

const labels = {
  TOURISM: '관광지',
  FOOD: '음식점·맛집',
  LODGING: '숙박',
  FESTIVAL: '축제·공연',
  COURSE: '여행코스',
  FREE: '자유',
}

onMounted(async () => {
  try {
    post.value = await postApi.detail(route.params.postId)
  } catch (loadError) {
    error.value = loadError.message
  } finally {
    loading.value = false
  }
})

async function remove(password) {
  try {
    await postApi.remove(route.params.postId, password)
    router.push('/community')
  } catch (removeError) {
    error.value = removeError.message
    modal.value = false
  }
}
</script>

<template>
  <section class="post-detail-page section">
    <div class="container post-detail-container">
      <RouterLink to="/community" class="back-link">
        <span aria-hidden="true">←</span> 여행 커뮤니티
      </RouterLink>

      <div v-if="loading" class="content-loading">
        <span />
        <strong>게시글을 불러오는 중입니다.</strong>
      </div>

      <div v-else-if="error && !post" class="error-panel" role="alert">
        <strong>게시글을 불러오지 못했습니다.</strong>
        <p>{{ error }}</p>
        <RouterLink to="/community" class="button secondary">목록으로</RouterLink>
      </div>

      <article v-else-if="post" class="post-article">
        <header class="post-article-header">
          <span class="category-chip">{{ labels[post.category] || post.category }}</span>
          <h1>{{ post.title }}</h1>
          <div class="post-article-meta">
            <span>{{ new Date(post.createdAt).toLocaleString('ko-KR') }}</span>
            <span>조회 {{ post.viewCount }}</span>
            <span>익명 여행자</span>
          </div>
        </header>

        <div class="post-article-body">{{ post.content }}</div>

        <div class="post-author-note">
          <span aria-hidden="true">i</span>
          <p>이 글은 사용자가 익명으로 작성한 커뮤니티 콘텐츠이며 공공 관광정보와 구분됩니다.</p>
        </div>

        <p v-if="error" class="error-text" role="alert">{{ error }}</p>

        <footer class="post-actions">
          <RouterLink to="/community" class="button secondary">목록으로</RouterLink>
          <div>
            <RouterLink :to="`/community/${post.id}/edit`" class="button secondary">수정</RouterLink>
            <button class="button danger" type="button" @click="modal = true">삭제</button>
          </div>
        </footer>
      </article>
    </div>

    <PasswordModal
      v-if="modal"
      title="게시글을 삭제할까요?"
      @close="modal = false"
      @confirm="remove"
    />
  </section>
</template>
