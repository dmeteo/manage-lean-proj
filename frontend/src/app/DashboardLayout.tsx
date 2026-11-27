import { Alert, Button, Layout } from 'antd'
import { useState } from 'react'
import { NavLink, Outlet } from 'react-router'
import { signOut } from '../api/auth'
import { isUnauthorized } from '../api/client'
import type { Role, UserDto } from '../api/types'
import { Brand } from '../components/Brand'

const roleLabels: Record<Role, string> = {
  admin: 'Администратор', coordinator: 'Координатор РЦК', manager: 'Руководитель проекта',
  approver: 'Согласующий', employee: 'Сотрудник',
}

export function DashboardLayout({ user, onSignedOut }: {
  user: UserDto; onSignedOut: () => void
}) {
  const [busy, setBusy] = useState(false)
  const [failed, setFailed] = useState(false)

  async function leave() {
    setBusy(true)
    setFailed(false)
    try {
      await signOut()
      onSignedOut()
    } catch (error) {
      if (isUnauthorized(error)) onSignedOut()
      else setFailed(true)
    } finally {
      setBusy(false)
    }
  }

  return (
    <Layout className="workspace">
      <aside className="sidebar">
        <Brand />
        <nav aria-label="Разделы кабинета">
          <NavLink to="/dashboard">Дашборд</NavLink>
          <NavLink to="/projects">Проекты</NavLink>
          <NavLink to="/activities">Мероприятия</NavLink>
        </nav>
      </aside>
      <Layout className="workspace-body">
        <header className="workspace-header">
          <div className="account">
            <strong>{user.displayName}</strong>
            <span>{roleLabels[user.role]}</span>
          </div>
          <Button loading={busy} onClick={() => void leave()}>Выйти</Button>
        </header>
        <Layout.Content className="workspace-content">
          {failed && <Alert showIcon type="error" title="Не удалось выйти. Попробуйте ещё раз." />}
          <Outlet />
        </Layout.Content>
      </Layout>
    </Layout>
  )
}
