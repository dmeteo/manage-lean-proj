import { request } from './client'
import type { LoginRequest, UserDto } from './types'

async function postSession<T>(path: 'login' | 'logout', body: LoginRequest | Record<string, never>) {
  const { csrfToken } = await request<{ csrfToken: string }>('/auth/csrf')
  return request<T>(`/auth/${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-CSRF-Token': csrfToken },
    body: JSON.stringify(body),
  })
}

export const getCurrentUser = (signal: AbortSignal) => request<UserDto>('/auth/me', { signal })
export const signIn = (input: LoginRequest) => postSession<UserDto>('login', input)
export const signOut = () => postSession<void>('logout', {})
