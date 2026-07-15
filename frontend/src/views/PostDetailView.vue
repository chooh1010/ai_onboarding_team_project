<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { postApi } from '../api/postApi'
import PasswordModal from '../components/community/PasswordModal.vue'

const route = useRoute(); const router = useRouter(); const post = ref(null); const modal = ref(false); const error = ref('')
onMounted(async () => { post.value = await postApi.detail(route.params.postId) })
async function remove(password) {
  try { await postApi.remove(route.params.postId, password); router.push('/community') }
  catch (e) { error.value = e.message; modal.value = false }
}
</script>

<template>
  <section v-if="post" class="section container post-detail">
    <RouterLink to="/community" class="back-link">← 커뮤니티</RouterLink>
    <header><span class="category-chip">{{ post.category }}</span><h1>{{ post.title }}</h1><p>{{ new Date(post.createdAt).toLocaleString('ko-KR') }} · 조회 {{ post.viewCount }}</p></header>
    <article>{{ post.content }}</article>
    <p v-if="error" class="error-text">{{ error }}</p>
    <div class="post-actions"><RouterLink :to="`/community/${post.id}/edit`" class="button ghost">수정</RouterLink><button class="button danger" @click="modal = true">삭제</button></div>
    <PasswordModal v-if="modal" title="게시글 삭제" @close="modal = false" @confirm="remove" />
  </section>
</template>
