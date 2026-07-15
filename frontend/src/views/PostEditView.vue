<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { postApi } from '../api/postApi'
import PostForm from '../components/community/PostForm.vue'
const route = useRoute(); const router = useRouter(); const post = ref(null); const error = ref('')
onMounted(async () => { post.value = await postApi.detail(route.params.postId) })
async function submit(payload) { try { const updated = await postApi.update(route.params.postId, payload); router.push(`/community/${updated.id}`) } catch (e) { error.value = e.message } }
</script>

<template><section v-if="post" class="section container form-page"><p class="eyebrow">Edit post</p><h1>게시글 수정</h1><p v-if="error" class="error-text">{{ error }}</p><PostForm :initial-value="{ category: post.category, title: post.title, content: post.content }" submit-label="수정하기" @submit="submit" /></section></template>
