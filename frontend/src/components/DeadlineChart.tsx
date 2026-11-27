import { Link } from 'react-router'
import type { ActivityDto } from '../api/types'
import { formatDate } from './formatDate'

export function DeadlineChart({ rows }: { rows: ActivityDto[] }) {
  const dates = new Map<string, number>()
  for (const { plannedEndDate, isOverdue } of rows) {
    const bucket = isOverdue ? 'overdue' : plannedEndDate
    dates.set(bucket, (dates.get(bucket) ?? 0) + 1)
  }
  const counts = [...dates].sort(([a], [b]) => a === 'overdue' ? -1 : b === 'overdue' ? 1 : a.localeCompare(b))
  const max = Math.max(1, ...dates.values())

  return (
    <section className="activities deadline-panel" aria-labelledby="deadlines-heading">
      <h2 id="deadlines-heading">Нагрузка по срокам</h2>
      <p className="panel-note">Количество мероприятий из списка ниже по плановым датам</p>
      {counts.length === 0 ? <p>Нет мероприятий</p> : (
        <ul className="deadline-list">
          {counts.map(([date, count]) => (
            <li key={date}>
              <Link to={date === 'overdue' ? '/activities?overdue=1' : `/activities?date=${encodeURIComponent(date)}`}>
                <span>{date === 'overdue' ? 'Просрочено' : formatDate(date)}</span>
                <span className="deadline-track" aria-hidden="true">
                  <span className={date === 'overdue' ? 'deadline-bar is-overdue' : 'deadline-bar'}
                    style={{ width: `${100 * count / max}%` }} />
                </span>
                <strong>{count}</strong>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}
