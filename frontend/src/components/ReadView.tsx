import { Alert, Button, Skeleton } from 'antd'
import { useEffect, useState } from 'react'
import type { ReactNode } from 'react'
import { ApiError, isUnauthorized, request } from '../api/client'

type Props<T> = { path: string; onSessionExpired: () => void; children: (data: T) => ReactNode }
type State<T> = { kind: 'loading' } | { kind: 'ready'; data: T } | { kind: 'error'; title: string }

export function ReadView<T>(props: Props<T>) {
  return <RequestView key={props.path} {...props} />
}

function RequestView<T>({ path, onSessionExpired, children }: Props<T>) {
  const [state, setState] = useState<State<T>>({ kind: 'loading' })
  const [attempt, setAttempt] = useState(0)

  useEffect(() => {
    const controller = new AbortController()
    void request<T>(path, { signal: controller.signal }).then(
      (data) => { if (!controller.signal.aborted) setState({ kind: 'ready', data }) },
      (error: unknown) => {
        if (controller.signal.aborted) return
        if (isUnauthorized(error)) {
          onSessionExpired()
          return
        }
        const title = error instanceof ApiError && error.status === 404 ? 'Запись не найдена'
          : error instanceof ApiError && error.status === 403 ? 'Нет доступа'
            : 'Не удалось загрузить данные'
        setState({ kind: 'error', title })
      },
    )
    return () => controller.abort()
  }, [path, onSessionExpired, attempt])

  if (state.kind === 'loading') return <Skeleton active aria-label="Загружаем данные" />
  if (state.kind === 'error') return <Alert type="error" showIcon title={state.title} action={
    <Button onClick={() => { setState({ kind: 'loading' }); setAttempt((value) => value + 1) }}>Повторить</Button>
  } />
  return children(state.data)
}
