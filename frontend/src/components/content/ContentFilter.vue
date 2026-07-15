<script setup>
import { computed, reactive, watch } from 'vue'

const props = defineProps({
  types: { type: Array, default: () => [] },
  areas: { type: Array, default: () => [] },
  modelValue: { type: Object, required: true },
})
const emit = defineEmits(['update:modelValue', 'search'])
const form = reactive({ ...props.modelValue })

watch(() => props.modelValue, (next) => Object.assign(form, next), { deep: true })
watch(form, () => emit('update:modelValue', { ...form }), { deep: true })

const areaOptions = computed(() => props.areas.flatMap((area) => [
  { label: area.name, areaCode: area.areaCode, sigunguCode: area.sigunguCode || '' },
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
</script>

<template>
  <form class="filter-panel" @submit.prevent="emit('search')">
    <label>
      콘텐츠 유형
      <select v-model="form.contentTypeId">
        <option value="">전체</option>
        <option v-for="type in types" :key="type.id" :value="type.id">{{ type.name }}</option>
      </select>
    </label>
    <label>
      지역
      <select :value="`${form.areaCode || ''}:${form.sigunguCode || ''}`" @change="selectArea">
        <option value=":">전체</option>
        <option v-for="area in areaOptions" :key="`${area.areaCode}:${area.sigunguCode}`" :value="`${area.areaCode}:${area.sigunguCode}`">
          {{ area.label }}
        </option>
      </select>
    </label>
    <label class="filter-keyword">
      검색어
      <input v-model.trim="form.keyword" placeholder="장소명 또는 주소" />
    </label>
    <label class="checkbox-label">
      <input
        v-model="form.hasImage"
        type="checkbox"
        :true-value="true"
        :false-value="null"
      />
      이미지가 있는 콘텐츠만
    </label>
    <button class="button primary" type="submit">검색</button>
  </form>
</template>
