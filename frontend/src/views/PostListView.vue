<script setup>
import { onMounted, reactive, ref } from 'vue'
import { postApi } from '../api/postApi'

const categories = [
  ['', '전체'], ['TOURISM', '관광지'], ['FOOD', '음식점·맛집'], ['LODGING', '숙박'],
  ['FESTIVAL', '축제·공연'], ['COURSE', '여행코스'], ['FREE', '자유'],
]
const filters = reactive({ category: '', keyword: '', page: 1, size: 10 })
const response = ref({ items: [], totalElements: 0, totalPages: 0, page: 1 })
const labels = Object.fromEntries(categories)
async function load() { response.value = await postApi.list(filters) }
async function search() { filters.page = 1; await load() }
async function move(page) { filters.page = page; await load() }
onMounted(load)
</script>

<template>
  <section class="page-hero compact"><div class="container"><p class="eyebrow">Community</p><h1>여행 커뮤니티</h1><p>익명으로 여행 정보와 경험을 나눠보세요.</p></div></section>
  <section class="section container">
    <div class="category-tabs">
      <button v-for="[value, label] in categories" :key="value" :class="{ active: filters.category === value }" @click="filters.category = value; search()">{{ label }}</button>
    </div>
    <form class="community-search" @submit.prevent="search">
      <input v-model.trim="filters.keyword" placeholder="제목 또는 내용 검색" />
      <button class="button primary">검색</button>
      <RouterLink to="/community/write" class="button dark">글쓰기</RouterLink>
    </form>
    <div class="community-table-wrap">
      <table class="community-table">
        <thead><tr><th>번호</th><th>카테고리</th><th>제목</th><th>작성일</th><th>조회</th></tr></thead>
        <tbody>
          <tr v-for="post in response.items" :key="post.id">
            <td>{{ post.id }}</td><td><span class="category-chip">{{ labels[post.category] }}</span></td>
            <td><RouterLink :to="`/community/${post.id}`">{{ post.title }}</RouterLink></td>
            <td>{{ new Date(post.createdAt).toLocaleDateString('ko-KR') }}</td><td>{{ post.viewCount }}</td>
          </tr>
          <tr v-if="!response.items.length"><td colspan="5" class="empty-cell">게시글이 없습니다.</td></tr>
        </tbody>
      </table>
    </div>
    <nav v-if="response.totalPages > 1" class="pagination"><button :disabled="response.page <= 1" @click="move(response.page - 1)">이전</button><span>{{ response.page }} / {{ response.totalPages }}</span><button :disabled="response.page >= response.totalPages" @click="move(response.page + 1)">다음</button></nav>
  </section>
</template>
