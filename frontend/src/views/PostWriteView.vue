<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { postApi } from '../api/postApi'
import PostForm from '../components/community/PostForm.vue'
const router = useRouter(); const error = ref('')
async function submit(payload) { try { const post = await postApi.create(payload); router.push(`/community/${post.id}`) } catch (e) { error.value = e.message } }
</script>

<template><section class="section container form-page"><p class="eyebrow">New post</p><h1>여행 이야기 쓰기</h1><p v-if="error" class="error-text">{{ error }}</p><PostForm @submit="submit" /></section></template>
