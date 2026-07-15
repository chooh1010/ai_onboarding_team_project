export const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/$/, '')

export async function apiFetch(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  })

  if (!response.ok) {
    let message = '요청 처리 중 오류가 발생했습니다.'
    try {
      const body = await response.json()
      message = typeof body.detail === 'string' ? body.detail : message
    } catch {
      // JSON 응답이 아니면 기본 메시지 사용
    }
    throw new Error(message)
  }

  if (response.status === 204) return null
  return response.json()
}

export function resolveImageUrl(url) {
  if (!url) return ''
  if (url.startsWith('http://')) {
    return `${API_BASE_URL}/api/images/proxy?url=${encodeURIComponent(url)}`
  }
  return url
}
