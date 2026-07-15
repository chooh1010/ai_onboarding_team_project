<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'

const props = defineProps({
  items: { type: Array, default: () => [] },
  totalCount: { type: Number, default: 0 },
  displayMax: { type: Number, default: 100 }, // 새 prop: 지도에 표시할 최대 갯수
})

const emit = defineEmits(['select-item', 'request-more'])
const mapContainer = ref(null)
const map = ref(null)
const markers = ref([])
const infoWindow = ref(null)
const mapError = ref('')

const mappedItems = computed(() => props.items || [])
const coordinateItems = computed(() => mappedItems.value.filter(isValidCoordinate))
// visibleItems는 displayMax를 따릅니다
const visibleItems = computed(() => coordinateItems.value.slice(0, props.displayMax))
const hasHiddenItems = computed(() => coordinateItems.value.length > props.displayMax)
const hasNoCoordinateItems = computed(() => mappedItems.value.length > coordinateItems.value.length)
// 실제 화면에 놓인 마커 수
const displayedCount = computed(() => markers.value.length)

function isValidCoordinate(item) {
  const lat = Number(item?.latitude)
  const lng = Number(item?.longitude)
  return Number.isFinite(lat) && Number.isFinite(lng) && lat !== 0 && lng !== 0
}

function loadKakaoMapSdk() {
  return new Promise((resolve, reject) => {
    if (window.kakao?.maps) {
      resolve()
      return
    }

    const existingScript = document.getElementById('kakao-map-sdk')
    if (existingScript) {
      // 이미 삽입된 스크립트의 load/error 이벤트 대기
      existingScript.addEventListener('load', () => resolve(), { once: true })
      existingScript.addEventListener('error', () => reject(new Error('카카오맵 SDK를 불러오지 못했습니다.')), { once: true })
      return
    }

    const appKey = import.meta.env.VITE_KAKAO_MAP_APP_KEY
    console.log('[KakaoMap] appKey exists:', Boolean(appKey))

    if (!appKey) {
      reject(new Error('VITE_KAKAO_MAP_APP_KEY가 설정되지 않았습니다.'))
      return
    }

    const script = document.createElement('script')
    script.id = 'kakao-map-sdk'
    script.src = `https://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${appKey}`
    script.async = true
    script.onload = () => resolve()
    script.onerror = (event) => {
      console.error('[KakaoMap] script load failed', event)
      reject(new Error('카카오맵 SDK를 불러오지 못했습니다.'))
    }

    document.head.appendChild(script)
  })
}

async function initMap() {
  if (!mapContainer.value) return

  try {
    await loadKakaoMapSdk()

    window.kakao.maps.load(() => {
      map.value = new window.kakao.maps.Map(mapContainer.value, {
        center: new window.kakao.maps.LatLng(35.1595, 126.8526),
        level: 10,
      })

      infoWindow.value = new window.kakao.maps.InfoWindow({ removable: false })
      renderMarkers()
      mapError.value = ''
    })
  } catch (error) {
    console.error('[KakaoMap] init failed', error)
    mapError.value = error.message || '지도를 불러올 수 없습니다.'
  }
}

function clearMarkers() {
  markers.value.forEach((marker) => marker.setMap(null))
  markers.value = []
}

function renderMarkers() {
  if (!map.value || !window.kakao?.maps) return

  clearMarkers()

  console.debug('[KakaoMap] renderMarkers counts', {
    items: mappedItems.value.length,
    coordinateItems: coordinateItems.value.length,
    visibleItems: visibleItems.value.length,
    displayMax: props.displayMax,
  })

  if (!visibleItems.value.length) {
    map.value.setCenter(new window.kakao.maps.LatLng(35.1595, 126.8526))
    map.value.setLevel(10)
    return
  }

  const bounds = new window.kakao.maps.LatLngBounds()

  visibleItems.value.forEach((item) => {
    const position = new window.kakao.maps.LatLng(Number(item.latitude), Number(item.longitude))
    const marker = new window.kakao.maps.Marker({ position, map: map.value })

    window.kakao.maps.event.addListener(marker, 'click', () => {
      infoWindow.value?.setContent(`
        <div style="padding:6px 8px; min-width:180px;">
          <strong>${item.title || '장소'}</strong><br/>
          <span>${item.address || '주소 정보 없음'}</span>
        </div>
      `)

      infoWindow.value?.open(map.value, marker)
      emit('select-item', item)
    })

    bounds.extend(position)
    markers.value.push(marker)
  })

  // 디버그: 실제 생성된 마커 수 출력
  console.debug('[KakaoMap] markers placed:', markers.value.length)

  map.value.setBounds(bounds)
}

watch(
  () => props.items,
  () => {
    if (map.value) renderMarkers()
  },
  { deep: true }
)

onMounted(() => initMap())
onBeforeUnmount(() => clearMarkers())
</script>

<template>
  <div class="map-panel">
    <div class="map-panel-header">
      <strong>지도에서 위치 확인</strong>
      <span>
        {{ props.totalCount ? `${props.totalCount}건 검색됨 · 지도 ${displayedCount}개` : '검색 결과가 없어요' }}
      </span>
    </div>
    <div v-if="mapError" class="map-empty">{{ mapError }}</div>
    <div v-else>
      <div v-if="hasNoCoordinateItems" class="map-helper">
        좌표가 없는 항목은 지도에서 제외되고, 표시 가능한 결과만 지도에 반영됩니다.
      </div>
      <div v-if="hasHiddenItems" class="map-helper">
        결과가 너무 많아 처음 {{ props.displayMax }}개만 지도에 표시됩니다.
        <!-- 부모에게 추가 로드를 요청할 수 있게 버튼 제공 -->
        <button class="map-more-btn" @click="$emit('request-more')">더 보기/전체 로드</button>
      </div>
      <div ref="mapContainer" class="map-container"></div>
    </div>
  </div>
</template>