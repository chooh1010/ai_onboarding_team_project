<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { contentApi } from '../api/contentApi'
import { resolveImageUrl } from '../api/http'

const route = useRoute()
const item = ref(null)
const failed = ref(false)
const image = computed(() => failed.value ? '' : resolveImageUrl(item.value?.firstImage || item.value?.firstImage2))
const mapLink = computed(() => item.value ? `https://www.google.com/maps?q=${item.value.latitude},${item.value.longitude}` : '#')
onMounted(async () => { item.value = await contentApi.detail(route.params.contentId) })
</script>

<template>
  <section v-if="item" class="detail-page container section">
    <RouterLink to="/explore" class="back-link">← 목록으로</RouterLink>
    <div class="detail-grid">
      <div class="detail-image">
        <img v-if="image" :src="image" :alt="`${item.title} 대표 이미지`" @error="failed = true" />
        <div v-else class="image-fallback large"><span>남도온</span><small>대표 이미지 없음</small></div>
      </div>
      <div class="detail-info">
        <span class="type-badge static">{{ item.contentTypeName }}</span>
        <h1>{{ item.title }}</h1>
        <dl>
          <div><dt>주소</dt><dd>{{ [item.addr1, item.addr2].filter(Boolean).join(' ') || '정보 없음' }}</dd></div>
          <div><dt>전화</dt><dd>{{ item.tel || '제공되지 않음' }}</dd></div>
          <div><dt>우편번호</dt><dd>{{ item.zipcode || '제공되지 않음' }}</dd></div>
          <div><dt>좌표</dt><dd>{{ item.latitude }}, {{ item.longitude }}</dd></div>
        </dl>
        <a class="button primary inline" :href="mapLink" target="_blank" rel="noreferrer">지도에서 위치 보기</a>
        <div class="source-box">
          <strong>데이터 출처</strong>
          <p>출처: {{ item.source.provider }}<br />라이선스: {{ item.source.license }}</p>
          <small>원본 데이터의 주소와 이미지는 임의로 변경하지 않았습니다.</small>
        </div>
      </div>
    </div>
  </section>
  <section v-else class="section container">불러오는 중…</section>
</template>
