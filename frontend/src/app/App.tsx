import { Alert, Button, Spin } from 'antd'
import { lazy, Suspense, useCallback, useEffect, useState } from 'react'
import { Navigate, Route, Routes } from 'react-router'
import { getCurrentUser } from '../api/auth'
import { isUnauthorized } from '../api/client'
import type { UserDto } from '../api/types'
import { LoginPage } from '../pages/LoginPage'
import { DashboardLayout } from './DashboardLayout'

const WorkspacePage = lazy(() => import('../pages/WorkspacePage'))
const ProjectsPage = lazy(() => import('../pages/ProjectsPage'))
const ProjectPage = lazy(() => import('../pages/ProjectPage'))
const ActivityPage = lazy(() => import('../pages/ActivityPage'))
const sections = ['dashboard', 'activities'] as const

type Session = { state: 'loading' | 'guest' | 'error' } | { state: 'signedIn'; user: UserDto }

export function App() {
  const [session, setSession] = useState<Session>({ state: 'loading' })
  const [attempt, setAttempt] = useState(0)
  const endSession = useCallback(() => setSession({ state: 'guest' }), [])

  useEffect(() => {
    const controller = new AbortController()
    void getCurrentUser(controller.signal).then(
      (user) => { if (!controller.signal.aborted) setSession({ state: 'signedIn', user }) },
      (error: unknown) => {
        if (!controller.signal.aborted) setSession({ state: isUnauthorized(error) ? 'guest' : 'error' })
      },
    )
    return () => controller.abort()
  }, [attempt])

  if (session.state === 'loading') return <main className="center"><Spin tip="Проверяем сеанс"><div className="spinner-space" /></Spin></main>
  if (session.state === 'error') {
    return <main className="center"><Alert type="error" title="Не удалось проверить сеанс" action={
      <Button onClick={() => { setSession({ state: 'loading' }); setAttempt((value) => value + 1) }}>Повторить</Button>
    } /></main>
  }

  return (
    <Routes>
      <Route path="/login" element={session.state === 'signedIn'
        ? <Navigate to="/dashboard" replace />
        : <LoginPage onSignedIn={(user) => setSession({ state: 'signedIn', user })} />} />
      <Route path="/" element={session.state === 'signedIn'
        ? <DashboardLayout user={session.user} onSignedOut={endSession} />
        : <Navigate to="/login" replace />}>
        <Route index element={<Navigate to="/dashboard" replace />} />
        {sections.map((section) => (
          <Route key={section} path={section} element={<Suspense fallback={<Spin aria-label="Загружаем раздел" />}>
            <WorkspacePage onSessionExpired={endSession} section={section} />
          </Suspense>} />
        ))}
        <Route path="projects" element={<Suspense fallback={<Spin aria-label="Загружаем реестр" />}>
          <ProjectsPage onSessionExpired={endSession} />
        </Suspense>} />
        <Route path="projects/:projectId" element={<Suspense fallback={<Spin aria-label="Загружаем проект" />}>
          <ProjectPage onSessionExpired={endSession} />
        </Suspense>} />
        <Route path="activities/:activityId" element={<Suspense fallback={<Spin aria-label="Загружаем мероприятие" />}>
          <ActivityPage onSessionExpired={endSession} />
        </Suspense>} />
      </Route>
      <Route path="*" element={<Navigate to={session.state === 'signedIn' ? '/dashboard' : '/login'} replace />} />
    </Routes>
  )
}
