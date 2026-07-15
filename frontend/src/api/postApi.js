import { apiFetch } from './http'

function query(params) {
  const search = new URLSearchParams()
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') search.set(key, value)
  })
  return search.toString()
}

export const postApi = {
  list: (params = {}) => apiFetch(`/api/posts?${query(params)}`),
  detail: (id) => apiFetch(`/api/posts/${id}`),
  create: (payload) => apiFetch('/api/posts', { method: 'POST', body: JSON.stringify(payload) }),
  update: (id, payload) => apiFetch(`/api/posts/${id}`, { method: 'PUT', body: JSON.stringify(payload) }),
  remove: (id, password) => apiFetch(`/api/posts/${id}`, { method: 'DELETE', body: JSON.stringify({ password }) }),
}
