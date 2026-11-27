import { Tag } from 'antd'
import type { ActivityDto, ActivityStatus } from '../api/types'

const statuses: Record<ActivityStatus, string> = {
  planned: 'Запланировано', inProgress: 'В работе', managerReview: 'На проверке',
  approverReview: 'На согласовании', returned: 'На доработке', internallyApproved: 'Согласовано',
}

export function ActivityStatusTag({ activity }: { activity: ActivityDto }) {
  const color = activity.isOverdue ? 'red' : activity.status === 'planned' ? 'default' : 'cyan'
  return <Tag color={color}>{activity.isOverdue ? 'Просрочено' : statuses[activity.status]}</Tag>
}
