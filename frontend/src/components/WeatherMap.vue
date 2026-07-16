<template>
  <div class="weather-widget-card">
    <div class="weather-widget-header">
      <div>
        <p class="weather-eyebrow">광주·전라권 날씨</p>
        <h4>현재 날씨</h4>
      </div>
      <button class="weather-detail-btn" type="button" @click="goToWeatherDetail">
        5일 예보 <i class="bi bi-arrow-right-short"></i>
      </button>
    </div>

    <div v-if="loading" class="weather-state-message" aria-live="polite">
      날씨를 불러오는 중입니다.
    </div>

    <div v-else-if="error" class="weather-state-message weather-error" role="alert">
      <strong>날씨를 불러오지 못했습니다.</strong>
      <span>{{ error }}</span>
    </div>

    <div v-else-if="weatherData.length" class="weather-summary-list">
      <div v-for="item in weatherData" :key="item.region_name" class="weather-summary-item">
        <span class="region-name-pill">{{ item.region_name }}</span>
        <span class="weather-summary-icon" :aria-label="translateWeather(item.weather_state)">
          <i class="bi" :class="getWeatherIcon(item.weather_state)"></i>
        </span>
        <span class="temp-pill">{{ formatTemperature(item.temp) }}°C</span>
      </div>
    </div>

    <div v-else class="weather-state-message">
      표시할 날씨 정보가 없습니다.
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { apiFetch } from '../api/http'

const weatherData = ref([])
const loading = ref(true)
const error = ref('')
const router = useRouter()

const getWeatherIcon = (state) => {
  const icons = {
    Clear: 'bi-sun-fill text-warning',
    Clouds: 'bi-cloud-sun-fill text-secondary',
    Rain: 'bi-cloud-rain-heavy-fill text-primary',
    Drizzle: 'bi-cloud-drizzle-fill text-info',
    Snow: 'bi-cloud-snow-fill text-info',
    Mist: 'bi-cloud-haze2-fill text-muted',
    Dust: 'bi-exclamation-triangle-fill text-danger',
    Haze: 'bi-cloud-haze2-fill text-muted',
    Thunderstorm: 'bi-cloud-lightning-rain-fill text-primary',
  }
  return icons[state] || 'bi-cloud-fill text-primary'
}

const translateWeather = (state) => ({
  Clear: '맑음',
  Clouds: '구름',
  Rain: '비',
  Drizzle: '이슬비',
  Snow: '눈',
  Mist: '안개',
  Dust: '먼지',
  Haze: '연무',
  Thunderstorm: '뇌우',
}[state] || state || '날씨')

const formatTemperature = (value) => {
  const number = Number(value)
  return Number.isFinite(number) ? Math.round(number) : '-'
}

const goToWeatherDetail = () => {
  router.push('/weather')
}

onMounted(async () => {
  try {
    const response = await apiFetch('/api/weather/current')
    weatherData.value = Array.isArray(response) ? response : []
  } catch (fetchError) {
    error.value = fetchError.message || '백엔드 연결과 API 키를 확인해 주세요.'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.weather-widget-card {
  width: 100%;
  max-width: 720px;
  margin: 0;
  border: 1px solid #e2e8f0;
  border-radius: 18px;
  padding: 16px;
  background: #ffffff;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.07);
}
.weather-widget-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}
.weather-eyebrow {
  margin: 0 0 2px;
  font-size: 0.72rem;
  font-weight: 700;
  color: #2563eb;
  letter-spacing: 0.04em;
}
.weather-widget-header h4 {
  margin: 0;
  font-size: 1rem;
  font-weight: 700;
  color: #0f172a;
}
.weather-detail-btn {
  border: none;
  border-radius: 999px;
  background: #2563eb;
  color: white;
  padding: 7px 11px;
  font-size: 0.78rem;
  font-weight: 600;
  cursor: pointer;
}
.weather-summary-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(132px, 1fr));
  gap: 8px;
}
.weather-summary-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 9px 10px;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  background: #f8fafc;
}
.region-name-pill {
  font-size: 0.8rem;
  font-weight: 700;
  color: #334155;
}
.weather-summary-icon {
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 18px;
}
.temp-pill {
  font-size: 0.82rem;
  font-weight: 700;
  color: #0f172a;
}
.weather-state-message {
  padding: 14px;
  border-radius: 10px;
  background: #f8fafc;
  color: #475569;
  font-size: 0.84rem;
}
.weather-error {
  display: grid;
  gap: 4px;
  background: #fff7ed;
  color: #9a3412;
}
</style>
