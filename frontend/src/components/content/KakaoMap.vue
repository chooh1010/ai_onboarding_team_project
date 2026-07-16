<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { API_BASE_URL } from '../../api/http'

const props = defineProps({
  items: { type: Array, default: () => [] },
})

const router = useRouter()
const mapContainer = ref(null)
const map = ref(null)
const markers = ref([])
const loading = ref(true)
const mapError = ref('')

function escapeHtml(value) {
  return String(value ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;')
}

async function resolveKakaoAppKey() {
  const buildTimeKey = String(import.meta.env.VITE_KAKAO_MAP_APP_KEY || '').trim()
  if (buildTimeKey) return buildTimeKey

  const response = await fetch(`${API_BASE_URL}/api/config/public`)
  if (!response.ok) {
    throw new Error('백엔드 공개 설정을 불러오지 못했습니다.')
  }

  const config = await response.json()
  const runtimeKey = String(config.kakaoMapAppKey || '').trim()
  if (!runtimeKey) {
    throw new Error('KAKAO_MAP_APP_KEY가 설정되지 않았습니다.')
  }
  return runtimeKey
}

function waitForExistingScript(existing) {
  return new Promise((resolve, reject) => {
    if (window.kakao?.maps) {
      window.kakao.maps.load(resolve)
      return
    }
    existing.addEventListener('load', () => window.kakao.maps.load(resolve), { once: true })
    existing.addEventListener('error', () => reject(new Error('카카오 지도 스크립트 로드 실패')), { once: true })
  })
}

async function loadKakaoScript() {
  if (window.kakao?.maps) {
    await new Promise(resolve => window.kakao.maps.load(resolve))
    return
  }

  const existing = document.querySelector('script[src*="dapi.kakao.com/v2/maps/sdk.js"]')
  if (existing) {
    await waitForExistingScript(existing)
    return
  }

  const appKey = await resolveKakaoAppKey()
  await new Promise((resolve, reject) => {
    const script = document.createElement('script')
    script.src = `https://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${encodeURIComponent(appKey)}`
    script.async = true
    script.onload = () => {
      if (!window.kakao?.maps) {
        reject(new Error('카카오 지도 SDK 초기화에 실패했습니다.'))
        return
      }
      window.kakao.maps.load(resolve)
    }
    script.onerror = () => reject(new Error('카카오 지도 스크립트 로드 실패'))
    document.head.appendChild(script)
  })
}

function clearMarkers() {
  markers.value.forEach(marker => marker.setMap(null))
  markers.value = []
}

const displayItems = computed(() => {
  const valid = (props.items || []).filter(item => {
    const lat = Number(item.latitude)
    const lng = Number(item.longitude)
    return Number.isFinite(lat) && Number.isFinite(lng)
  })
  return valid.slice(0, 100)
})

function drawMarkers() {
  if (!map.value || !window.kakao?.maps) return

  clearMarkers()
  const validItems = displayItems.value

  if (!validItems.length) {
    map.value.setCenter(new window.kakao.maps.LatLng(35.1595, 126.8526))
    map.value.setLevel(8)
    return
  }

  const bounds = new window.kakao.maps.LatLngBounds()

  validItems.forEach(item => {
    const position = new window.kakao.maps.LatLng(Number(item.latitude), Number(item.longitude))
    const marker = new window.kakao.maps.Marker({
      position,
      map: map.value,
      title: item.title,
    })
    const infowindow = new window.kakao.maps.InfoWindow({
      content: `<div style="padding:8px 12px;font-size:13px;">${escapeHtml(item.title)}</div>`,
    })

    window.kakao.maps.event.addListener(marker, 'click', () => {
      if (item.contentId) {
        router.push(`/contents/${item.contentId}`)
      } else {
        infowindow.open(map.value, marker)
      }
    })

    bounds.extend(position)
    markers.value.push(marker)
  })

  map.value.setBounds(bounds)
}

const markerCount = computed(() => displayItems.value.length)

onMounted(async () => {
  try {
    await loadKakaoScript()
    map.value = new window.kakao.maps.Map(mapContainer.value, {
      center: new window.kakao.maps.LatLng(35.1595, 126.8526),
      level: 8,
    })
    drawMarkers()
  } catch (error) {
    console.error(error)
    mapError.value = `${error.message} 카카오 개발자 콘솔의 JavaScript 키와 배포 도메인 등록도 확인해 주세요.`
  } finally {
    loading.value = false
  }
})

watch(() => props.items, () => drawMarkers(), { deep: true })
</script>

<template>
  <div class="kakao-map-card">
    <div ref="mapContainer" class="kakao-map-container" />
    <div v-if="loading" class="map-status">지도를 불러오는 중입니다.</div>
    <div v-else-if="mapError" class="map-status map-error" role="alert">
      <strong>지도를 표시하지 못했습니다.</strong>
      <span>{{ mapError }}</span>
    </div>
    <div v-if="!mapError" class="map-badge" aria-label="지도 표시 장소 수">{{ markerCount }}</div>
  </div>
</template>

<style scoped>
.kakao-map-card {
  margin-bottom: 24px;
  border-radius: 28px;
  overflow: hidden;
  border: 1px solid #e4ebe5;
  background: #fff;
  box-shadow: 0 14px 35px rgba(17, 42, 27, 0.08);
  position: relative;
}
.kakao-map-container {
  width: 100%;
  min-height: 360px;
  height: 100%;
}
.map-status {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 28px;
  background: rgba(248, 250, 252, 0.96);
  color: #475569;
  text-align: center;
  font-size: 14px;
}
.map-error {
  flex-direction: column;
  gap: 8px;
  color: #9a3412;
  background: rgba(255, 247, 237, 0.97);
}
.map-error span {
  max-width: 680px;
  line-height: 1.6;
}
.map-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  background: rgba(0, 0, 0, 0.65);
  color: #fff;
  font-weight: 600;
  font-size: 13px;
  padding: 6px 10px;
  border-radius: 999px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.12);
  pointer-events: none;
}
</style>
