<template>
  <div class="container my-5">
    <div class="d-flex justify-content-between align-items-center mb-4 p-3 bg-white rounded-4 shadow-sm border border-light">
      <div class="d-flex align-items-center gap-3">
        <div class="header-icon bg-primary text-white rounded-3 p-2">
          <i class="bi bi-cloud-sun fs-4"></i>
        </div>
        <div>
          <h3 class="fw-bold m-0 text-dark-blue">광주·전라권 5일 예보</h3>
        </div>
      </div>
      <button class="btn btn-primary px-3 rounded-pill fw-bold" @click="$router.push('/')">
        <i class="bi bi-geo-alt-fill me-1"></i> 메인 페이지로 이동
      </button>
    </div>

    <div class="row g-4 mb-4">
      <div class="col-lg-8">
        <div class="card border-0 rounded-4 shadow-sm text-white h-100 bg-dark-gradient position-relative overflow-hidden p-4">
          <div class="d-flex align-items-center gap-3 mb-3 position-relative z-index-2">
            <span class="fs-2">💡</span>
            <h5 class="fw-bold m-0">전라남도 관광 매칭 가이드</h5>
          </div>
          <p class="mb-0 text-light-opacity position-relative z-index-2 lh-lg">
            {{ recommendComment || "날씨 분석기 가동 중..." }}
          </p>
        </div>
      </div>
      
      <div class="col-lg-4">
        <div class="card border-0 rounded-4 shadow-sm h-100 p-4 bg-white border border-light">
          <h6 class="fw-bold text-secondary mb-3"><i class="bi bi-activity me-1"></i> 야외 활동 지수</h6>
          <div class="d-flex align-items-center gap-4">
            <div class="progress-circle" :style="{ '--percent': activityScore }">
              <span class="fw-extrabold text-dark fs-3">{{ activityScore }}%</span>
            </div>
            <div>
              <span class="badge bg-success-subtle text-success rounded-pill mb-1 px-3 py-2 fw-bold fs-7">
                {{ activityScore >= 70 ? '활동 원활' : '실내 추천' }}
              </span>
              <p class="small text-muted mb-0 mt-1">자외선 지수 및 종합 습도를 계산한 지수입니다.</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="card border-0 rounded-4 shadow-sm p-4 mb-4 bg-white border border-light">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h5 class="fw-bold text-dark-blue m-0"><i class="bi bi-graph-up text-primary me-2"></i> 최고/최저 기온 추이 그래프</h5>
        <span class="small text-muted">단위: °C</span>
      </div>
      <div class="chart-container py-4">
        <div class="d-flex justify-content-between text-center align-items-stretch h-100 px-2">
          <div v-for="(day, index) in weeklyForecast" :key="index" class="chart-bar-column d-flex flex-column justify-content-between align-items-center">
            <span class="text-danger fw-bold small mb-1">{{ day.maxTemp }}°</span>
            
            <div class="bar-wrapper-box d-flex align-items-end justify-content-center flex-grow-1 my-2">
              <div class="temperature-trend-bar" :style="{ height: Math.max((day.maxTemp - day.minTemp) * 8, 15) + 'px' }"></div>
            </div>
            
            <span class="text-primary fw-bold small mt-1">{{ day.minTemp }}°</span>
            <span class="text-secondary extra-small mt-2 fw-semibold">{{ getWeekdayLabel(day.dayOfWeek) }}</span>
          </div>
        </div>
      </div>
    </div>

    <h5 class="fw-bold text-dark-blue mb-3"><i class="bi bi-calendar3 text-primary me-2"></i> 5일간의 상세 기상 예보</h5>
    <div class="row row-cols-2 row-cols-md-4 row-cols-lg-7 g-3">
      <div v-for="(day, index) in weeklyForecast" :key="index" class="col">
        <div class="card h-100 border-0 shadow-sm text-center forecast-card rounded-4 bg-white" :class="{ 'today-card': index === 0 }">
          <div class="card-header bg-transparent border-0 pt-3">
            <span class="badge rounded-pill px-3 py-1.5" :class="index === 0 ? 'bg-primary' : 'bg-light text-secondary'">
              {{ index === 0 ? '오늘' : getWeekdayLabel(day.dayOfWeek) }}
            </span>
            <div class="small text-muted mt-2 fw-semibold">{{ day.date }}</div>
          </div>
          <div class="card-body py-2">
            <div class="weather-icon-box my-3">
              <i class="bi" :class="getWeatherIcon(day.state)"></i>
            </div>
            <div class="fw-bold text-dark mb-1">{{ translateState(day.state) }}</div>
          </div>
          <div class="card-footer bg-transparent border-0 pb-3">
            <div class="d-flex justify-content-center gap-2 small">
              <span class="text-danger fw-bold fs-6">{{ day.maxTemp }}°</span>
              <span class="text-muted fs-6">/</span>
              <span class="text-primary fw-bold fs-6">{{ day.minTemp }}°</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { apiFetch } from '../api/http'

const weeklyForecast = ref([]);
const recommendComment = ref('');
const activityScore = ref(0);

const getWeekdayLabel = (value) => {
  const weekdayMap = {
    '월': '月',
    '화': '火',
    '수': '水',
    '목': '木',
    '금': '金',
    '토': '土',
    '일': '日',
    'Monday': '月',
    'Tuesday': '火',
    'Wednesday': '水',
    'Thursday': '木',
    'Friday': '金',
    'Saturday': '土',
    'Sunday': '日',
    '월요일': '月',
    '화요일': '火',
    '수요일': '水',
    '목요일': '木',
    '금요일': '金',
    '토요일': '土',
    '일요일': '日',
  };

  return weekdayMap[value] || value || '';
};

const getWeatherIcon = (state) => {
  const icons = {
    'Clear': 'bi-sun-fill text-warning fs-1',
    'Clouds': 'bi-cloud-sun-fill text-secondary fs-1',
    'Rain': 'bi-cloud-rain-heavy-fill text-primary fs-1',
    'Snow': 'bi-cloud-snow-fill text-info fs-1',
    'Haze': 'bi-cloud-haze2-fill text-muted fs-1'
  };
  return icons[state] || 'bi-cloud-fill text-secondary fs-1';
};

const translateState = (state) => {
  const koState = { 'Clear': '맑음', 'Clouds': '구름많음', 'Rain': '비', 'Snow': '눈', 'Haze': '안개' };
  return koState[state] || '흐림';
};

onMounted(async () => {
  try {
    const res = await apiFetch('/api/weather/forecast')
    if (res && Array.isArray(res.items)) {
      weeklyForecast.value = res.items
    }

    const todayState = weeklyForecast.value[0]?.state || 'Clouds'
    const hasDust = weeklyForecast.value[0]?.has_dust

    if (hasDust) {
      recommendComment.value = "⚠️ 오늘 초미세먼지 농도가 높습니다. 마스크를 착용하시고 실내 활동을 고려하세요."
      activityScore.value = 40;
    } else if (todayState === 'Clear') {
      recommendComment.value = "🟢 오늘은 하늘이 맑고 쾌적하여 야외 여행에 최적화된 기후입니다.";
      activityScore.value = 95;
    } else if (todayState === 'Rain') {
      recommendComment.value = "🚨 광주 전역에 강수가 예보되어 있으니 우산을 챙기시기 바랍니다.";
      activityScore.value = 35;
    } else {
      recommendComment.value = "🟡 구름이 다소 끼어 선선한 날씨입니다.";
      activityScore.value = 75;
    }
  } catch (e) {
    // leave demo text if fetch fails
    console.warn('Failed to load weekly forecast', e)
    weeklyForecast.value = weeklyForecast.value || []
  }
})
</script>

<style scoped>
.text-dark-blue {
  color: #1e3a8a;
}
.bg-dark-gradient {
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
}
.text-light-opacity {
  color: #cbd5e1;
}
.extra-small {
  font-size: 0.75rem;
}

/* 주간 기온 트렌드 바 정렬 레이아웃 버그 수정 */
.chart-container {
  background-color: #f8fafc;
  border-radius: 12px;
  height: 220px; /* 전체 차트 높이 안정화 */
}
.chart-bar-column {
  flex: 1;
  height: 100%;
}
.bar-wrapper-box {
  width: 100%;
  height: 100px; /* 막대가 유동적으로 늘어날 수 있는 독립적 최대 높이 바운더리 지정 */
}
.temperature-trend-bar {
  width: 14px;
  background: linear-gradient(to top, #3b82f6, #ef4444);
  border-radius: 20px;
  transition: all 0.3s ease;
}

/* 예보 카드 모션 */
.forecast-card {
  transition: transform 0.2s, box-shadow 0.2s;
  border: 1px solid #f1f5f9;
}
.forecast-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.08) !important;
}
.today-card {
  border: 2px solid #3b82f6 !important;
  background-color: #f0f6ff !important;
}

/* 원형 프로그레스 바 UI */
.progress-circle {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  background: conic-gradient(#3b82f6 calc(var(--percent) * 1%), #e2e8f0 0);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}
.progress-circle::before {
  content: "";
  position: absolute;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: #ffffff;
}
.progress-circle span {
  position: relative;
  z-index: 2;
}
</style>