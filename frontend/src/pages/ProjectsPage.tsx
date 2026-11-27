import { Input, Progress, Table, Tag } from 'antd'
import type { TableColumnsType } from 'antd'
import { Link, useSearchParams } from 'react-router'
import type { Page, ProjectDto } from '../api/types'
import { formatDate } from '../components/formatDate'
import { ReadView } from '../components/ReadView'

const labels: Record<ProjectDto['status'], string> = {
  active: 'В работе', draft: 'Черновик', completed: 'Завершён', archived: 'В архиве',
}

const columns: TableColumnsType<ProjectDto> = [
  { title: 'Проект', key: 'name', render: (_, project) => <Link to={`/projects/${project.id}`}>{project.name}</Link> },
  { title: 'Предприятие', dataIndex: 'enterpriseName' },
  { title: 'Руководитель', dataIndex: 'managerName' },
  { title: 'Статус', dataIndex: 'status', render: (status: ProjectDto['status']) => <Tag>{labels[status]}</Tag> },
  { title: 'Плановый срок', dataIndex: 'plannedEndDate', render: formatDate },
  { title: 'Готовность', dataIndex: 'progressPercent', width: 140,
    render: (value: number) => <Progress percent={value} size="small" /> },
]

export default function ProjectsPage({ onSessionExpired }: { onSessionExpired: () => void }) {
  const [params, setParams] = useSearchParams()
  const page = Math.max(1, Number(params.get('page')) || 1)
  const search = params.get('search') ?? ''
  const query = new URLSearchParams({ page: String(page), pageSize: '20' })
  if (search) query.set('search', search)

  return <>
    <div className="page-heading"><h1>Проекты</h1><p>Реестр проектов и состояние работ</p></div>
    <section className="activities" aria-label="Реестр проектов">
      <Input.Search className="registry-search" aria-label="Поиск по названию проекта" placeholder="Поиск по названию проекта"
        key={search} defaultValue={search} allowClear onSearch={(value) => setParams(value.trim() ? { search: value.trim() } : {})} />
      <ReadView<Page<ProjectDto>> path={`/projects?${query}`} onSessionExpired={onSessionExpired}>
        {(result) => <Table rowKey="id" columns={columns} dataSource={result.items} scroll={{ x: 900 }}
          locale={{ emptyText: 'Проекты не найдены' }}
          pagination={{ current: result.page, pageSize: result.pageSize, total: result.total,
            showSizeChanger: false, hideOnSinglePage: true,
            onChange: (next) => setParams(search ? { page: String(next), search } : { page: String(next) }) }} />}
      </ReadView>
    </section>
  </>
}
