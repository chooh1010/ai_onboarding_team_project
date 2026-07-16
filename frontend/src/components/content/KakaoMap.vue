<script setup>
import { onMounted, ref, watch, computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  items: { type: Array, default: () => [] }
})

const router = useRouter()
const mapContainer = ref(null)
const map = ref(null)
const markers = ref([])

function loadKakaoScript() {
  return new Promise((resolve, reject) => {
    if (window.kakao?.maps) {
      resolve()
      return
    }

    const existing = document.querySelector('script[src*="dapi.kakao.com/v2/maps/sdk.js"]')
    if (existing) {
      existing.addEventListener('load', () => window.kakao.maps.load(resolve), { once: true })
      existing.addEventListener('error', () => reject(new Error('카카오 스크립트 로드 실패')), { once: true })
      return
    }

    const appKey = import.meta.env.VITE_KAKAO_MAP_APP_KEY
    if (!appKey) {
      reject(new Error('VITE_KAKAO_MAP_APP_KEY 환경 변수가 설정되지 않았습니다.'))
      return
    }

    const script = document.createElement('script')
    script.src = `https://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${appKey}`
    script.onload = () => window.kakao.maps.load(resolve)
    script.onerror = () => reject(new Error('카카오 스크립트 로드 실패'))
    document.head.appendChild(script)
  })
}

function clearMarkers() {
  markers.value.forEach(marker => marker.setMap(null))
  markers.value = []
}

// 유효 좌표 필터링 + 최대 100개 제한
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
    const position = new window.kakao.maps.LatLng(item.latitude, item.longitude)

    const marker = new window.kakao.maps.Marker({
      position,
      map: map.value,
      title: item.title
    })

    const infowindow = new window.kakao.maps.InfoWindow({
      content: `<div style="padding:8px 12px;font-size:13px;">${item.title}</div>`
    })

    // 클릭: 상세 페이지로 이동(없으면 인포윈도우만 연다)
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
      level: 8
    })

    drawMarkers()
  } catch (err) {
    console.error(err)
  }
})

watch(() => props.items, () => drawMarkers(), { deep: true })
</script>

<template>
  <div class="kakao-map-card">
    <div ref="mapContainer" class="kakao-map-container" />
    <div class="map-badge" aria-hidden="true">{{ markerCount }}</div>
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
.map-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  background: rgba(0,0,0,0.65);
  color: #fff;
  font-weight: 600;
  font-size: 13px;
  padding: 6px 10px;
  border-radius: 999px;
  box-shadow: 0 6px 18px rgba(0,0,0,0.12);
  pointer-events: none;
}
</style>