import type { ActivityDto, DashboardDto, ProjectDto, UserDto } from '../api/types'

export const account = { login: 'm.volkova', password: 'LeanProject2026!' }
export const user: UserDto = {
  id: 'b17f3e5a-82fb-4b56-8e5e-2d12ab8b743f',
  displayName: 'Марина Волкова',
  login: account.login,
  role: 'manager',
  enterpriseId: null,
  isActive: true,
  version: 1,
}

export const projects: ProjectDto[] = ([
  { id: '0d109c94-f18e-467f-bc37-94f1e090f188', name: 'Сокращение времени переналадки',
    enterpriseName: 'Вектор-Механика', status: 'active', startDate: '2026-11-16',
    plannedEndDate: '2026-12-18', actualEndDate: null, progressPercent: 33,
    description: 'Сократить время подготовки оборудования к смене серии.' },
  { id: 'bc81cdab-db33-4974-9933-240412607f5a', name: 'Оптимизация маршрута комплектации',
    enterpriseName: 'Промконтур', status: 'active', startDate: '2026-11-20',
    plannedEndDate: '2026-12-21', actualEndDate: null, progressPercent: 0,
    description: 'Уменьшить время перемещения при комплектации заказов.' },
  { id: 'b6f03ff4-0610-4b24-8dc6-4d84e2a04cc1', name: 'Снижение ожидания материалов',
    enterpriseName: 'Вектор-Механика', status: 'draft', startDate: '2026-12-03',
    plannedEndDate: '2027-01-15', actualEndDate: null, progressPercent: 0, description: null },
] satisfies Omit<ProjectDto, 'managerName'>[]).map((project) => ({ ...project, managerName: user.displayName }))

const asOf = '2026-11-27T09:00:00+05:00'
const activityRows = [
  { id: 'c0be0b66-3af1-4293-89a4-3d897b3c78a7', projectId: projects[0].id,
    title: 'Определить границы пилотного участка', plannedEndDate: '2026-11-20', status: 'internallyApproved', actualEndDate: '2026-11-19' },
  { id: '22aaf7db-e1c6-40cf-bce3-94def6dd27f7', projectId: projects[0].id,
    title: 'Провести замер времени переналадки', plannedEndDate: '2026-11-25', status: 'inProgress', actualEndDate: null },
  { id: '77ced283-adff-4816-be2a-a200c6a9c5e1', projectId: projects[0].id,
    title: 'Проверить карту текущего потока', plannedEndDate: '2026-11-27', status: 'managerReview', actualEndDate: '2026-11-27' },
  { id: 'd28fbd2b-ca42-4081-a2a5-26ebb827b9cd', projectId: projects[1].id,
    title: 'Согласовать схему зоны комплектации', plannedEndDate: '2026-11-30', status: 'planned', actualEndDate: null },
  { id: 'f087e27b-3906-4b1f-ad04-aa897af8ab74', projectId: projects[1].id,
    title: 'Проверить комплектность рабочих мест', plannedEndDate: '2026-11-30', status: 'inProgress', actualEndDate: null },
] satisfies Pick<ActivityDto, 'id' | 'projectId' | 'title' | 'plannedEndDate' | 'actualEndDate' | 'status'>[]

export const activities: ActivityDto[] = activityRows.map((activity) => ({
  ...activity,
  plannedStartDate: projects.find(({ id }) => id === activity.projectId)?.startDate ?? null,
  stage: 'Диагностика и планирование',
  assigneeName: 'Алексей Орлов',
  comment: activity.status === 'managerReview' ? 'Карта потока подготовлена и передана руководителю.' : null,
  isOverdue: activity.plannedEndDate < asOf.slice(0, 10) && activity.actualEndDate === null,
}))

const upcomingActivities = activities.filter(({ status }) => status !== 'internallyApproved')
export const dashboard: DashboardDto = {
  activeProjects: projects.filter(({ status }) => status === 'active').length,
  inProgressActivities: activities.filter(({ status }) => status === 'inProgress').length,
  overdueActivities: upcomingActivities.filter(({ isOverdue }) => isOverdue).length,
  pendingReviews: activities.filter(({ status }) => status === 'managerReview').length,
  upcomingActivities,
  asOf,
}
