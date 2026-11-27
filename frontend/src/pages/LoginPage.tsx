import { Alert, Button, Form, Input } from 'antd'
import { useState } from 'react'
import { signIn } from '../api/auth'
import { isUnauthorized } from '../api/client'
import type { LoginRequest, UserDto } from '../api/types'
import { Brand } from '../components/Brand'

export function LoginPage({ onSignedIn }: { onSignedIn: (user: UserDto) => void }) {
  const [busy, setBusy] = useState(false)
  const [errorText, setErrorText] = useState('')

  async function submit(values: LoginRequest) {
    setBusy(true)
    setErrorText('')
    try {
      onSignedIn(await signIn({ ...values, login: values.login.trim() }))
    } catch (error) {
      setErrorText(isUnauthorized(error) ? 'Неверный логин или пароль.' : 'Не удалось войти. Попробуйте ещё раз.')
    } finally {
      setBusy(false)
    }
  }

  return (
    <main className="login">
      <section className="login-brand" aria-label="Lean Project">
        <Brand />
        <div className="login-identity">
          <span>Региональный центр компетенций</span>
          <p>Управление<br /> lean-проектами</p>
        </div>
        <div className="process-lines" aria-hidden="true"><i /><i /><i /></div>
      </section>
      <section className="login-content">
        <div className="login-form">
          <h1>Вход в систему</h1>
          <p>Войдите под своей учётной записью.</p>
          <Form<LoginRequest> layout="vertical" disabled={busy} onFinish={(input) => void submit(input)}>
            <Form.Item label="Логин" name="login" rules={[{ required: true, whitespace: true, message: 'Введите логин' }]}>
              <Input size="large" autoComplete="username" />
            </Form.Item>
            <Form.Item label="Пароль" name="password" rules={[{ required: true, message: 'Введите пароль' }]}>
              <Input.Password size="large" autoComplete="current-password" />
            </Form.Item>
            {errorText && <Alert className="login-error" showIcon type="error" title={errorText} />}
            <Button size="large" type="primary" htmlType="submit" loading={busy} block>Войти</Button>
          </Form>
        </div>
      </section>
    </main>
  )
}
