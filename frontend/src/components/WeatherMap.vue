//  메인용 날씨 지도 시각화 컴포넌트

<template>
  <div class="weather-widget-card">
    <div class="weather-widget-header">
      <div>
        <p class="weather-eyebrow">광주 권역 날씨</p>
        <h4>현재 날씨</h4>
      </div>
      <button class="weather-detail-btn" type="button" @click="goToWeatherDetail">
        7일 예보 <i class="bi bi-arrow-right-short"></i>
      </button>
    </div>

    <div class="weather-summary-list" v-if="weatherData.length">
      <div v-for="item in weatherData" :key="item.region_name" class="weather-summary-item">
        <span class="region-name-pill">{{ item.region_name }}</span>
        <span class="weather-summary-icon">
          <i class="bi" :class="getWeatherIcon(item.weather_state)"></i>
        </span>
        <span class="temp-pill">{{ item.temp }}°C</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const weatherData = ref([]);
const router = useRouter();

// 1) 돌아다닐 때 영향을 주는 날씨 상태 코드별 아이콘 매핑 (Bootstrap Icons 기준)
const getWeatherIcon = (state) => {
  const icons = {
    'Clear': 'bi-sun-fill text-warning',
    'Clouds': 'bi-cloud-sun-fill text-secondary',
    'Rain': 'bi-cloud-rain-heavy-fill text-primary',
    'Drizzle': 'bi-cloud-drizzle-fill text-info',
    'Snow': 'bi-cloud-snow-fill text-info',
    'Mist': 'bi-cloud-haze2-fill text-muted',
    'Dust': 'bi-exclamation-triangle-fill text-danger',
    'Haze': 'bi-cloud-haze2-fill text-muted'
  };
  return icons[state] || 'bi-cloud-fill text-primary';
};

const goToWeatherDetail = () => {
  router.push('/weather');
};

onMounted(async () => {
  try {
    const response = await axios.get(`${import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'}/api/weather/current`);

    if (response.data && Array.isArray(response.data)) {
      weatherData.value = response.data;
    } else if (response.data && response.data.data && Array.isArray(response.data.data)) {
      weatherData.value = response.data.data;
    } else {
      weatherData.value = [];
      console.warn("응답 데이터가 예상된 배열 포맷이 아닙니다.");
    }
  } catch (error) {
    console.error("날씨 데이터를 불러오지 못했습니다:", error);
  }
});
</script>

<style scoped>
.weather-widget-card {
  width: 100%;
  max-width: 280px;
  margin: 0;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 10px 12px;
  background: #ffffff;
  box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06);
}
.weather-widget-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}
.weather-eyebrow {
  margin: 0 0 1px;
  font-size: 0.68rem;
  font-weight: 700;
  color: #2563eb;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}
.weather-widget-header h4 {
  margin: 0;
  font-size: 0.9rem;
  font-weight: 700;
  color: #0f172a;
}
.weather-detail-btn {
  border: none;
  border-radius: 999px;
  background: #2563eb;
  color: white;
  padding: 5px 8px;
  font-size: 0.76rem;
  font-weight: 600;
  cursor: pointer;
}
.weather-summary-list {
  display: grid;
  gap: 5px;
}
.weather-summary-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 6px 8px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: #f8fafc;
}
.region-name-pill {
  font-size: 0.78rem;
  font-weight: 700;
  color: #334155;
}
.weather-summary-icon {
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 18px;
}
.temp-pill {
  font-size: 0.8rem;
  font-weight: 700;
  color: #0f172a;
}
</style>