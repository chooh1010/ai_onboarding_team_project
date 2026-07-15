<script setup>
import { onMounted, ref } from 'vue'
import { apiFetch } from '../api/http'

const source = ref(null)
const error = ref('')

onMounted(async () => {
  try {
    source.value = await apiFetch('/api/data-source')
  } catch (loadError) {
    error.value = loadError.message
  }
})
</script>

<template>
  <section class="page-hero source-page-hero">
    <div class="container page-hero-inner">
      <div>
        <span class="page-hero-label">데이터와 라이선스</span>
        <h1>여행정보의 출처와<br />확인할 수 있는 범위를 안내합니다.</h1>
        <p>남도온은 제공된 공공데이터 밖의 정보를 임의로 만들어내지 않습니다.</p>
      </div>
      <span class="source-page-seal" aria-hidden="true">公</span>
    </div>
  </section>

  <section class="section source-page-section">
    <div class="container">
      <div v-if="error" class="error-panel" role="alert">
        <strong>데이터 출처 정보를 불러오지 못했습니다.</strong>
        <p>{{ error }}</p>
      </div>

      <template v-else-if="source">
        <div class="source-summary-grid">
          <article class="source-summary-card primary-card">
            <span class="section-label">기본 정보</span>
            <h2>{{ source.datasetName }}</h2>
            <p>{{ source.attributionText }}</p>
            <dl>
              <div><dt>제공 기관</dt><dd>{{ source.provider }}</dd></div>
              <div><dt>API</dt><dd>{{ source.apiName }}</dd></div>
              <div><dt>서비스 권역</dt><dd>{{ source.region }}</dd></div>
              <div><dt>수집일</dt><dd>{{ source.collectedAt || source.collectedAtNote }}</dd></div>
            </dl>
          </article>

          <article class="source-summary-card license-card">
            <span class="source-seal" aria-hidden="true">3</span>
            <span class="section-label">이용 조건</span>
            <h2>{{ source.licenseName }}</h2>
            <dl>
              <div><dt>상업적 이용</dt><dd>{{ source.commercialUse ? '가능' : '불가' }}</dd></div>
              <div><dt>원본 내용 변경</dt><dd>{{ source.modificationAllowed ? '가능' : '금지' }}</dd></div>
              <div><dt>출처 표시</dt><dd>필수</dd></div>
            </dl>
            <a class="button primary" :href="source.sourceUrl" target="_blank" rel="noreferrer">
              공공데이터 원본 보기 <span aria-hidden="true">↗</span>
            </a>
          </article>
        </div>

        <article class="data-principles">
          <div class="section-heading split-heading">
            <div>
              <span class="section-label">원본 보존 원칙</span>
              <h2>화면에서도 원본 데이터의 의미를 지킵니다.</h2>
            </div>
            <p>공공누리 제3유형의 이용 조건에 따라 관광정보와 사용자 작성 데이터를 명확하게 구분합니다.</p>
          </div>
          <div class="principle-grid">
            <div><span>01</span><strong>원본 주소 보존</strong><p>일반적이지 않은 표현이 있어도 임의로 고치지 않습니다.</p></div>
            <div><span>02</span><strong>원본 이미지 보존</strong><p>이미지 URL을 다른 이미지로 덮어쓰지 않습니다.</p></div>
            <div><span>03</span><strong>날짜 의미 구분</strong><p>등록·수정 시각을 축제 개최일로 해석하지 않습니다.</p></div>
            <div><span>04</span><strong>사용자 글 구분</strong><p>커뮤니티 게시글과 공공 관광정보를 명확히 구분합니다.</p></div>
          </div>
        </article>

        <article class="limitation-card">
          <div>
            <span class="section-label">데이터 한계</span>
            <h2>현재 데이터만으로 확인할 수 없는 정보</h2>
            <p>챗봇도 아래 내용을 추측해서 답변하지 않습니다.</p>
          </div>
          <ul>
            <li><strong>축제 일정</strong><span>시작일·종료일, 행사 기간과 운영 시간</span></li>
            <li><strong>음식점 상세</strong><span>모범음식점 여부, 메뉴, 가격, 영업시간과 휴무일</span></li>
            <li><strong>여행코스 경로</strong><span>구성 장소, 방문 순서, 총 거리와 이동 시간</span></li>
            <li><strong>감성 추천 근거</strong><span>상세 소개문을 전제로 하는 데이트·가족 여행 추천</span></li>
          </ul>
        </article>
      </template>

      <div v-else class="content-loading">
        <span />
        <strong>데이터 출처 정보를 불러오는 중입니다.</strong>
      </div>
    </div>
  </section>
</template>
