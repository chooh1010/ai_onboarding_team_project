import { apiFetch } from './http'

export const chatApi = {
  send: (message, history = []) => apiFetch('/api/chat', {
    method: 'POST',
    body: JSON.stringify({ message, history }),
  }),
}
