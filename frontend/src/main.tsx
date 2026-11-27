import { ConfigProvider } from 'antd'
import ruRU from 'antd/locale/ru_RU'
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router'
import { App } from './app/App'
import './styles.css'

async function start() {
  const root = createRoot(document.getElementById('root')!)
  try {
    if (import.meta.env.DEV && import.meta.env.MODE === 'demo') {
      const { worker } = await import('./mocks/browser')
      await worker.start({
        onUnhandledRequest(request, print) {
          if (new URL(request.url).pathname.startsWith('/api/')) print.error()
        },
      })
    }
  } catch (error) {
    console.error(error)
    root.render(<main className="center" role="alert">Не удалось запустить приложение. Обновите страницу.</main>)
    return
  }
  root.render(
    <StrictMode>
      <ConfigProvider locale={ruRU} theme={{ token: { colorPrimary: '#116a5a', borderRadius: 8, fontFamily: 'inherit' } }}>
        <BrowserRouter><App /></BrowserRouter>
      </ConfigProvider>
    </StrictMode>,
  )
}

void start()
