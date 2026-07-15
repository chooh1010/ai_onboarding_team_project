<script setup>
import { onMounted, ref } from 'vue'
import { apiFetch } from '../api/http'
const source = ref(null)
onMounted(async () => { source.value = await apiFetch('/api/data-source') })
</script>

<template>
  <section class="page-hero compact"><div class="container"><p class="eyebrow">Data & License</p><h1>데이터 출처 안내</h1><p>서비스가 사용하는 데이터의 범위와 한계를 투명하게 안내합니다.</p></div></section>
  <section v-if="source" class="section container source-page">
    <div class="source-grid">
      <article><h2>기본 정보</h2><dl><div><dt>제공 기관</dt><dd>{{ source.provider }}</dd></div><div><dt>데이터명</dt><dd>{{ source.datasetName }}</dd></div><div><dt>API</dt><dd>{{ source.apiName }}</dd></div><div><dt>권역</dt><dd>{{ source.region }}</dd></div><div><dt>수집일</dt><dd>{{ source.collectedAt || source.collectedAtNote }}</dd></div></dl></article>
      <article><h2>라이선스</h2><dl><div><dt>유형</dt><dd>{{ source.licenseName }}</dd></div><div><dt>상업적 이용</dt><dd>{{ source.commercialUse ? '가능' : '불가' }}</dd></div><div><dt>원본 변경</dt><dd>{{ source.modificationAllowed ? '가능' : '금지' }}</dd></div></dl><a class="button primary inline" :href="source.sourceUrl" target="_blank" rel="noreferrer">공공데이터 원본 보기</a></article>
    </div>
    <article class="limitation-card"><h2>현재 데이터로 확인할 수 없는 정보</h2><ul><li>축제 시작일·종료일과 행사 기간</li><li>모범음식점 지정 여부, 위생등급, 메뉴·가격·영업시간</li><li>여행코스 구성 장소, 방문 순서, 총 거리와 이동 시간</li><li>상세 소개문을 전제로 한 감성·상황 추천</li></ul><p>챗봇도 위 정보를 추측해서 답하지 않습니다.</p></article>
  </section>
</template>
