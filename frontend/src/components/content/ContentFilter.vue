<script setup>
import { computed, reactive, watch } from 'vue'

const props = defineProps({
  types: {
    type: Array,
    default: () => [],
  },
  areas: {
    type: Array,
    default: () => [],
  },
  modelValue: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['update:modelValue', 'search'])
const form = reactive({ ...props.modelValue })

watch(
  () => props.modelValue,
  (next) => Object.assign(form, next),
  { deep: true },
)

watch(
  form,
  () => emit('update:modelValue', { ...form }),
  { deep: true },
)

const areaOptions = computed(() => props.areas.flatMap((area) => [
  {
    label: area.name,
    areaCode: area.areaCode,
    sigunguCode: area.sigunguCode || '',
  },
  ...(area.children || []).map((child) => ({
    label: `광주 ${child.name}`,
    areaCode: child.areaCode,
    sigunguCode: child.sigunguCode,
  })),
]))

function selectArea(event) {
  const [areaCode = '', sigunguCode = ''] = event.target.value.split(':')
  form.areaCode = areaCode
  form.sigunguCode = sigunguCode
}

function reset() {
  Object.assign(form, {
    contentTypeId: '',
    areaCode: '',
    sigunguCode: '',
    keyword: '',
    hasImage: null,
    page: 1,
  })
  emit('search')
}
</script>

<template>
  <form class="filter-panel" @submit.prevent="emit('search')">
    <div class="filter-heading">
      <div>
        <span class="section-label">여행지 찾기</span>
        <strong>어디로, 어떤 여행을 떠날까요?</strong>
      </div>
      <button type="button" class="filter-reset" @click="reset">
        조건 초기화
      </button>
    </div>

    <div class="filter-fields">
      <label class="field-group">
        <span>콘텐츠 유형</span>
        <select v-model="form.contentTypeId">
          <option value="">전체 유형</option>
          <option
            v-for="type in types"
            :key="type.id"
            :value="type.id"
          >
            {{ type.name }} ({{ type.count.toLocaleString() }})
          </option>
        </select>
      </label>

      <label class="field-group">
        <span>지역</span>
        <select
          :value="`${form.areaCode || ''}:${form.sigunguCode || ''}`"
          @change="selectArea"
        >
          <option value=":">광주·전라권 전체</option>
          <option
            v-for="area in areaOptions"
            :key="`${area.areaCode}:${area.sigunguCode}`"
            :value="`${area.areaCode}:${area.sigunguCode}`"
          >
            {{ area.label }}
          </option>
        </select>
      </label>

      <label class="field-group filter-keyword">
        <span>검색어</span>
        <span class="filter-input-wrap">
          <span aria-hidden="true">⌕</span>
          <input
            v-model.trim="form.keyword"
            placeholder="장소명 또는 주소를 입력하세요"
          />
        </span>
      </label>

      <label class="checkbox-label">
        <input
          v-model="form.hasImage"
          type="checkbox"
          :true-value="true"
          :false-value="null"
        />
        <span class="custom-check" aria-hidden="true" />
        <span>
          <strong>사진이 있는 장소만</strong>
          <small>선택하지 않으면 전체 장소가 표시됩니다.</small>
        </span>
      </label>

      <button class="button primary filter-submit" type="submit">
        검색 결과 보기 <span aria-hidden="true">→</span>
      </button>
    </div>
  </form>
</template>
