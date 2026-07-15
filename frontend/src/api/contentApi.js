import { apiFetch } from './http'

function toQuery(params) {
  const search = new URLSearchParams()

  Object.entries(params).forEach(([key, value]) => {
    if (
      value !== undefined &&
      value !== null &&
      value !== '' &&
      value !== false
    ) {
      search.set(key, value)
    }
  })

  return search.toString()
}

export const contentApi = {
  types: () => apiFetch('/api/content-types'),
  areas: () => apiFetch('/api/areas'),
  list: (params = {}) => apiFetch(`/api/contents?${toQuery(params)}`),
  detail: (contentId) => apiFetch(`/api/contents/${contentId}`),
  nearby: (params) => apiFetch(`/api/contents/nearby?${toQuery(params)}`),
}
