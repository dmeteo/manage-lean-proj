import { Table } from 'antd'
import type { TableColumnsType } from 'antd'
import { useState } from 'react'
import { Link, useParams } from 'react-router'
import type { ActivityDto, Page, ProjectDto } from '../api/types'
import { ActivityStatusTag } from '../components/ActivityStatusTag'
import { formatDate } from '../components/formatDate'
import { ReadView } from '../components/ReadView'

const columns: TableColumnsType<ActivityDto> = [
  { title: 'Мероприятие', key: 'title', render: (_, row) => <Link to={`/activities/${row.id}`}>{row.title}</Link> },
  { title: 'Этап', dataIndex: 'stage', render: (value) => value ?? '—' },
  { title: 'Плановый срок', dataIndex: 'plannedEndDate', render: formatDate },
  { title: 'Факт завершения', dataIndex: 'actualEndDate', render: (value) => value ? formatDate(value) : '—' },
  { title: 'Статус', key: 'status', render: (_, row) => <ActivityStatusTag activity={row} /> },
]

export default function ProjectPage({ onSessionExpired }: { onSessionExpired: () => void }) {
  const { projectId = '' } = useParams()
  const path = `/projects/${encodeURIComponent(projectId)}`
  return <ReadView<ProjectDto> path={path} onSessionExpired={onSessionExpired}>
    {(project) => <ProjectDetails key={project.id} project={project} path={path} onSessionExpired={onSessionExpired} />}
  </ReadView>
}

function ProjectDetails({ project, path, onSessionExpired }: {
  project: ProjectDto; path: string; onSessionExpired: () => void
}) {
  const [page, setPage] = useState(1)
  return <>
    <div className="page-heading">
      <Link to="/projects">Все проекты</Link>
      <h1>{project.name}</h1>
      <p>{project.enterpriseName} · {project.managerName}</p>
      {project.description && <p>{project.description}</p>}
    </div>
    <section className="activities detail-section" aria-labelledby="plan-heading">
      <h2 id="plan-heading">План проекта</h2>
      <p className="panel-note">Начало {formatDate(project.startDate)} · План завершения {formatDate(project.plannedEndDate)}
        {project.actualEndDate ? ` · Завершён ${formatDate(project.actualEndDate)}` : ''}</p>
      <ReadView<Page<ActivityDto>> path={`${path}/activities?page=${page}&pageSize=20`} onSessionExpired={onSessionExpired}>
        {(result) => <Table rowKey="id" columns={columns} dataSource={result.items} scroll={{ x: 800 }}
          locale={{ emptyText: 'В плане пока нет мероприятий' }}
          pagination={{ current: result.page, pageSize: result.pageSize, total: result.total,
            hideOnSinglePage: true, showSizeChanger: false, onChange: setPage }} />}
      </ReadView>
    </section>
  </>
}
