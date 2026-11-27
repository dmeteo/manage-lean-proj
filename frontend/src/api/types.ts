export type Role = 'admin' | 'coordinator' | 'manager' | 'approver' | 'employee'
export type ActivityStatus = 'planned' | 'inProgress' | 'managerReview' | 'approverReview' | 'returned' | 'internallyApproved'

export interface LoginRequest { login: string; password: string }
export interface UserDto {
  id: string
  displayName: string
  login: string
  role: Role
  enterpriseId: string | null
  isActive: boolean
  version: number
}

export interface ActivityDto {
  id: string
  projectId: string
  title: string
  plannedEndDate: string
  plannedStartDate: string | null
  actualEndDate: string | null
  assigneeName: string
  stage: string | null
  comment: string | null
  status: ActivityStatus
  isOverdue: boolean
}

export interface DashboardDto {
  activeProjects: number
  inProgressActivities: number
  overdueActivities: number
  pendingReviews: number
  upcomingActivities: ActivityDto[]
  asOf: string
}

export interface ProjectDto {
  id: string
  name: string
  enterpriseName: string
  managerName: string
  startDate: string
  plannedEndDate: string
  actualEndDate: string | null
  status: 'draft' | 'active' | 'completed' | 'archived'
  progressPercent: number
  description: string | null
}

export interface Page<T> { items: T[]; page: number; pageSize: number; total: number }
export interface DocumentDto { id: string; originalName: string; revision: number }
export interface ReviewDto {
  id: string
  stage: 'manager' | 'approver'
  decision: 'approve' | 'return'
  comment: string | null
  createdAt: string
}
