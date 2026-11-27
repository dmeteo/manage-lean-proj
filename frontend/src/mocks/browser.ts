import { http, HttpResponse } from 'msw'
import { setupWorker } from 'msw/browser'
import { account, activities, dashboard, projects, user } from './fixtures'

const sessionKey = 'lean:mock-session'
let csrfToken = ''
const hasSession = () => sessionStorage.getItem(sessionKey) === user.id

function problem(status: number, title: string, code: string) {
  return HttpResponse.json({ type: 'about:blank', status, title, code }, {
    status,
    headers: { 'Content-Type': 'application/problem+json' },
  })
}

const unauthorized = () => problem(401, 'Требуется вход', 'unauthorized')
const invalidCsrf = () => problem(403, 'Не удалось проверить запрос', 'csrf_invalid')
const validCsrf = (request: Request) => csrfToken && request.headers.get('X-CSRF-Token') === csrfToken

function list<T>(items: T[], request: Request) {
  const params = new URL(request.url).searchParams
  const page = Math.max(1, Number(params.get('page')) || 1)
  const pageSize = Math.min(100, Math.max(1, Number(params.get('pageSize')) || 20))
  const offset = (page - 1) * pageSize
  return HttpResponse.json({ items: items.slice(offset, offset + pageSize), page, pageSize, total: items.length })
}

export const worker = setupWorker(
  http.get('/api/auth/csrf', () => {
    csrfToken = crypto.randomUUID()
    return HttpResponse.json({ csrfToken })
  }),
  http.post('/api/auth/login', async ({ request }) => {
    if (!validCsrf(request)) return invalidCsrf()
    const input = await request.json() as { login?: string; password?: string } | null
    if (input?.login !== account.login || input.password !== account.password) return unauthorized()
    sessionStorage.setItem(sessionKey, user.id)
    csrfToken = ''
    return HttpResponse.json(user)
  }),
  http.get('/api/auth/me', () => hasSession() ? HttpResponse.json(user) : unauthorized()),
  http.post('/api/auth/logout', ({ request }) => {
    if (!hasSession()) return unauthorized()
    if (!validCsrf(request)) return invalidCsrf()
    sessionStorage.removeItem(sessionKey)
    csrfToken = ''
    return new HttpResponse(null, { status: 204 })
  }),
  http.get('/api/dashboard', () => hasSession() ? HttpResponse.json(dashboard) : unauthorized()),
  http.get('/api/projects', ({ request }) => {
    if (!hasSession()) return unauthorized()
    const search = new URL(request.url).searchParams.get('search')?.toLocaleLowerCase('ru') ?? ''
    return list(projects.filter(({ name }) => name.toLocaleLowerCase('ru').includes(search)), request)
  }),
  http.get('/api/projects/:id', ({ params }) => {
    if (!hasSession()) return unauthorized()
    const project = projects.find(({ id }) => id === params.id)
    return project ? HttpResponse.json(project) : problem(404, 'Проект не найден', 'not_found')
  }),
  http.get('/api/projects/:id/activities', ({ params, request }) => {
    if (!hasSession()) return unauthorized()
    if (!projects.some(({ id }) => id === params.id)) return problem(404, 'Проект не найден', 'not_found')
    return list(activities.filter(({ projectId }) => projectId === params.id), request)
  }),
  http.get('/api/activities/:id', ({ params }) => {
    if (!hasSession()) return unauthorized()
    const activity = activities.find(({ id }) => id === params.id)
    return activity ? HttpResponse.json(activity) : problem(404, 'Мероприятие не найдено', 'not_found')
  }),
  http.get('/api/activities/:id/files', ({ params, request }) => {
    if (!hasSession()) return unauthorized()
    const activity = activities.find(({ id }) => id === params.id)
    if (!activity) return problem(404, 'Мероприятие не найдено', 'not_found')
    const documents = activity.status === 'managerReview'
      ? [{ id: '497f6df1-eeb2-4cca-9e93-dc5564df31c1', originalName: 'Карта текущего потока.pdf', revision: 1 }] : []
    return list(documents, request)
  }),
  http.get('/api/activities/:id/reviews', ({ params, request }) => {
    if (!hasSession()) return unauthorized()
    const activity = activities.find(({ id }) => id === params.id)
    if (!activity) return problem(404, 'Мероприятие не найдено', 'not_found')
    const reviews = activity.status === 'internallyApproved'
      ? [
          { id: '80db410a-7d05-4d18-80fc-f6a871d90582', stage: 'manager', decision: 'approve', comment: 'Границы участка подтверждены.', createdAt: '2026-11-19T13:00:00+05:00' },
          { id: 'd6dd2d8d-e5a7-4af6-9a7e-7bbb91237910', stage: 'approver', decision: 'approve', comment: null, createdAt: '2026-11-19T15:00:00+05:00' },
        ] : []
    return list(reviews, request)
  }),
)
