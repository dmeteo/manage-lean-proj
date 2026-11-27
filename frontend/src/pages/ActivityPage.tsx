import { Pagination } from 'antd'
import { useState } from 'react'
import type { ReactNode } from 'react'
import { Link, useParams } from 'react-router'
import type { ActivityDto, DocumentDto, Page, ReviewDto } from '../api/types'
import { ActivityStatusTag } from '../components/ActivityStatusTag'
import { formatDate } from '../components/formatDate'
import { ReadView } from '../components/ReadView'

export default function ActivityPage({ onSessionExpired }: { onSessionExpired: () => void }) {
  const { activityId = '' } = useParams()
  const path = `/activities/${encodeURIComponent(activityId)}`
  return <ReadView<ActivityDto> path={path} onSessionExpired={onSessionExpired}>
    {(activity) => <>
      <div className="page-heading">
        <Link to={`/projects/${activity.projectId}`}>К плану проекта</Link>
        <h1>{activity.title}</h1>
        <p>{activity.stage ?? 'Этап не указан'}</p>
      </div>
      <section className="activities detail-section" aria-label="Сведения о мероприятии">
        <ActivityStatusTag activity={activity} />
        <dl className="detail-grid">
          <div><dt>Ответственный</dt><dd>{activity.assigneeName}</dd></div>
          <div><dt>Плановое начало</dt><dd>{activity.plannedStartDate ? formatDate(activity.plannedStartDate) : '—'}</dd></div>
          <div><dt>Плановый срок</dt><dd>{formatDate(activity.plannedEndDate)}</dd></div>
          <div><dt>Факт завершения</dt><dd>{activity.actualEndDate ? formatDate(activity.actualEndDate) : '—'}</dd></div>
        </dl>
        {activity.comment && <p>{activity.comment}</p>}
      </section>
      <ActivityRecords<DocumentDto> key={`${activity.id}-files`} title="Документы" path={`${path}/files`}
        onSessionExpired={onSessionExpired} empty="Документы пока не прикреплены"
        render={(item) => <>{item.originalName} · версия {item.revision}</>} />
      <ActivityRecords<ReviewDto> key={`${activity.id}-reviews`} title="История проверки" path={`${path}/reviews`}
        onSessionExpired={onSessionExpired} empty="Решений по проверке пока нет"
        render={(item) => <>
          <strong>{item.stage === 'manager' ? 'Проверка руководителя' : 'Согласование'} — {item.decision === 'approve' ? 'принято' : 'возвращено'}</strong>
          <p>{new Intl.DateTimeFormat('ru-RU', { dateStyle: 'medium', timeStyle: 'short', timeZone: 'Asia/Yekaterinburg' }).format(new Date(item.createdAt))}</p>
          {item.comment && <p>{item.comment}</p>}
        </>} />
    </>}
  </ReadView>
}

function ActivityRecords<T extends { id: string }>({ title, path, onSessionExpired, render, empty }: {
  title: string; path: string; onSessionExpired: () => void; render: (item: T) => ReactNode; empty: string
}) {
  const [page, setPage] = useState(1)
  return <section className="activities detail-section" aria-label={title}>
    <h2>{title}</h2>
    <ReadView<Page<T>> path={`${path}?page=${page}&pageSize=20`} onSessionExpired={onSessionExpired}>
      {(data) => data.items.length ? <>
        <ul className="detail-records">{data.items.map((item) => <li key={item.id}>{render(item)}</li>)}</ul>
        <Pagination current={data.page} pageSize={data.pageSize} total={data.total}
          onChange={setPage} showSizeChanger={false} hideOnSinglePage />
      </> : <p>{empty}</p>}
    </ReadView>
  </section>
}
