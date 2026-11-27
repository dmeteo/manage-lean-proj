import { ApiError, isUnauthorized, request } from './client'
import type { DashboardDto, ProjectDto } from './types'

export async function getDashboard(signal: AbortSignal) {
  const summary = await request<DashboardDto>('/dashboard', { signal })
  const ids = [...new Set(summary.upcomingActivities.map(({ projectId }) => projectId))]
  const names = await Promise.all(ids.map(async (id) => {
    try {
      const project = await request<ProjectDto>(`/projects/${encodeURIComponent(id)}`, { signal })
      return [id, project.name] as const
    } catch (error) {
      if (signal.aborted || isUnauthorized(error)) throw error
      if (error instanceof ApiError && error.status === 403) throw error
      return [id, null] as const
    }
  }))
  return { ...summary, projectNames: new Map<string, string | null>(names) }
}
