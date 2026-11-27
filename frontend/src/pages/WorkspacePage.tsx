import { Alert, Button, Empty, Select, Skeleton, Table } from 'antd'
import type { TableColumnsType } from 'antd'
import { useEffect, useState } from 'react'
import { Link, useSearchParams } from 'react-router'
import { isUnauthorized } from '../api/client'
import { getDashboard } from '../api/dashboard'
import type { ActivityDto } from '../api/types'
import { ActivityStatusTag } from '../components/ActivityStatusTag'
import { DeadlineChart } from '../components/DeadlineChart'
import { formatDate } from '../components/formatDate'

type Summary = Awaited<ReturnType<typeof getDashboard>>
type View = { state: 'loading' | 'error' } | { state: 'ready'; summary: Summary }
type Section = keyof typeof sections
const sections = {
  dashboard: { title: 'Дашборд', description: 'Состояние проектов и ближайшие сроки' },
  activities: { title: 'Мероприятия', description: 'Мероприятия из сводки по срокам' },
}

export default function WorkspacePage({ onSessionExpired, section }: {
  onSessionExpired: () => void
  section: Section
}) {
  const [view, setView] = useState<View>({ state: 'loading' })
  const [attempt, setAttempt] = useState(0)

  useEffect(() => {
    const controller = new AbortController()
    void getDashboard(controller.signal).then(
      (summary) => { if (!controller.signal.aborted) setView({ state: 'ready', summary }) },
      (error: unknown) => {
        if (controller.signal.aborted) return
        if (isUnauthorized(error)) onSessionExpired()
        else setView({ state: 'error' })
      },
    )
    return () => controller.abort()
  }, [attempt, onSessionExpired])

  return (
    <>
      <div className="page-heading">
        <h1>{sections[section].title}</h1>
        <p>{sections[section].description}</p>
      </div>
      {view.state === 'loading' && <Skeleton active aria-label="Загружаем сводку" />}
      {view.state === 'error' && <Alert type="error" showIcon title="Не удалось загрузить сводку" action={
        <Button onClick={() => { setView({ state: 'loading' }); setAttempt((value) => value + 1) }}>Повторить</Button>
      } />}
      {view.state === 'ready' && (
        section === 'activities' ? <ActivitiesOverview summary={view.summary} /> : <DashboardSummary summary={view.summary} />
      )}
    </>
  )
}

function DashboardSummary({ summary }: { summary: Summary }) {
  const metrics = [
    { label: 'Активные проекты', value: summary.activeProjects, tone: 'normal' },
    { label: 'Срок в ближайшие 7 дней', value: summary.upcomingActivities.filter((row) => isDueSoon(row, summary.asOf)).length, tone: 'normal', link: '/activities?scope=week', note: 'В сводке' },
    { label: 'На проверке', value: summary.pendingReviews, tone: 'review', link: '/activities?scope=review' },
    { label: 'Просрочено', value: summary.overdueActivities, tone: 'overdue', link: '/activities?overdue=1' },
  ]
  return (
    <>
      <dl className="metrics">
        {metrics.map(({ label, value, tone, link, note }) => (
          <div className={`metric metric--${tone}`} key={label}><dt>{link ? <Link to={link}>{label}</Link> : label}</dt><dd>{value}</dd>{note && <dd className="metric-note">{note}</dd>}</div>
        ))}
      </dl>
      <DeadlineChart rows={summary.upcomingActivities} />
      <section className="activities" aria-labelledby="activity-heading">
        <div className="panel-heading">
          <h2 id="activity-heading">Мероприятия и сроки</h2>
          <Link to="/activities">Открыть список</Link>
        </div>
        <ActivityTable rows={summary.upcomingActivities} names={summary.projectNames} />
      </section>
    </>
  )
}

function ActivitiesOverview({ summary }: { summary: Summary }) {
  const [params, setParams] = useSearchParams()
  const project = params.get('project')
  const date = params.get('date')
  const isOverdue = params.get('overdue') === '1'
  const requestedScope = params.get('scope')
  const scope = isOverdue ? 'overdue' : date ? `date:${date}` : requestedScope === 'week' || requestedScope === 'review' ? requestedScope : 'all'
  const options = [
    { value: 'all', label: 'Все сроки' },
    { value: 'overdue', label: 'Просрочено' },
    { value: 'week', label: 'Ближайшие 7 дней' },
    { value: 'review', label: 'На проверке' },
    ...(date && !isOverdue ? [{ value: scope, label: formatDate(date) }] : []),
  ]
  const rows = summary.upcomingActivities.filter((row) =>
    (!project || row.projectId === project) && (!isOverdue || row.isOverdue) &&
    (isOverdue || !date || (!row.isOverdue && row.plannedEndDate === date)) &&
    (scope !== 'week' || isDueSoon(row, summary.asOf)) &&
    (scope !== 'review' || row.status === 'managerReview' || row.status === 'approverReview'))

  function setFilter(key: string, value: string | null) {
    setParams((current) => {
      const next = new URLSearchParams(current)
      if (value) next.set(key, value)
      else next.delete(key)
      return next
    })
  }

  return <section className="activities" aria-label="Список мероприятий">
    <div className="activity-filters">
      <Select aria-label="Проект" value={project ?? ''}
        options={[{ value: '', label: 'Все проекты' }, ...[...summary.projectNames].map(([id, name]) => ({
          value: id, label: name ?? 'Название недоступно',
        }))]}
        onChange={(value) => setFilter('project', value || null)} />
      <Select aria-label="Срок или статус" value={scope} options={options} onChange={(value) => {
        if (value.startsWith('date:')) return
        const next = new URLSearchParams()
        if (project) next.set('project', project)
        if (value === 'overdue') next.set('overdue', '1')
        if (value === 'review' || value === 'week') next.set('scope', value)
        setParams(next)
      }} />
    </div>
    <ActivityTable rows={rows} names={summary.projectNames} />
  </section>
}

function ActivityTable({ rows, names }: { rows: ActivityDto[]; names: Summary['projectNames'] }) {
  const columns: TableColumnsType<ActivityDto> = [
    { title: 'Мероприятие', key: 'title', width: '34%',
      render: (_, row) => <Link to={`/activities/${row.id}`}>{row.title}</Link> },
    { title: 'Проект', key: 'project', render: (_, row) => names.get(row.projectId) ? <Link to={`/projects/${row.projectId}`}>{names.get(row.projectId)}</Link> : 'Название недоступно' },
    { title: 'Плановый срок', dataIndex: 'plannedEndDate', width: 140,
      render: (date: string) => <time dateTime={date}>{formatDate(date)}</time> },
    { title: 'Статус', key: 'status', width: 150,
      render: (_, row) => <ActivityStatusTag activity={row} /> },
  ]

  return <Table rowKey="id" columns={columns} dataSource={rows} pagination={false}
    scroll={{ x: 700 }} locale={{ emptyText: <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description="Нет мероприятий" /> }} />
}

function isDueSoon(activity: ActivityDto, asOf: string) {
  const localDate = new Intl.DateTimeFormat('sv-SE', { timeZone: 'Asia/Yekaterinburg' }).format(new Date(asOf))
  const day = Date.parse(activity.plannedEndDate) - Date.parse(localDate)
  return !activity.isOverdue && day >= 0 && day < 7 * 86_400_000
}
