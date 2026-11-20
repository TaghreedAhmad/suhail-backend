import type { Report, Stats, Verdict } from './types'

const BASE_URL = (import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000').replace(/\/$/, '')

interface ApiReport {
  report_id: string
  clip_id?: string | null
  filename?: string
  media_type?: 'image' | 'video' | 'audio' | 'unknown'
  is_demo?: boolean
  job_status: string
  verdict: Verdict | null
  authenticity_score: number | null
  certainty: 'low' | 'medium' | 'high' | null
  segments: { start_sec: number; end_sec: number; reason: string }[]
  reasons: string[]
  recommendations: string[]
  model_version?: string | null
  created_at?: string | null
}

async function request<T>(path: string): Promise<T> {
  const inviteCode = sessionStorage.getItem('suhail_invite_code')

  const response = await fetch(`${BASE_URL}${path}`, {
    headers: inviteCode
      ? { 'X-Invite-Code': inviteCode }
      : {},
  })

  if (!response.ok) {
    throw new Error(`خطأ من الخادم: ${response.status}`)
  }

  return response.json() as Promise<T>
}
function mapReport(item: ApiReport): Report {
  return {
    id: item.report_id,
    filename: item.filename ?? 'ملف غير معروف',
    media_type: item.media_type ?? 'unknown',
    created_at: item.created_at ?? null,
    verdict: item.verdict,
    authenticity_score: item.authenticity_score,
    certainty: item.certainty,
    status: item.job_status,
    reasons: item.reasons ?? [],
    recommendations: item.recommendations ?? [],
    segments: (item.segments ?? []).map(segment => ({
      start: segment.start_sec,
      end: segment.end_sec,
      note: segment.reason,
    })),
    model_version: item.model_version ?? null,
  }
}


export const api = {
  health: () => request<{ status: string }>('/health'),

  reports: async (): Promise<Report[]> => {
    return request<ApiReport[]>('/reports').then(items => items.map(mapReport))
  },

  report: async (id: string): Promise<Report> => {
    const result = await request<ApiReport>(
      `/reports/${encodeURIComponent(id)}`
    )
    return mapReport(result)
  },

  stats: () => request<Stats>('/stats'),

analyze: async (file: File, onProgress: (value: number) => void): Promise<Report> => {
  const inviteCode = sessionStorage.getItem('suhail_invite_code')
  if (!inviteCode) throw new Error('أدخلي رمز الدعوة أولاً.')

  const data = new FormData()
  data.append('file', file)

  onProgress(30)

  const response = await fetch(`${BASE_URL}/upload`, {
    method: 'POST',
    headers: { 'X-Invite-Code': inviteCode },
    body: data,
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || `خطأ من الخادم: ${response.status}`)
  }

  const result = await response.json()
  onProgress(100)

  return {
    id: result.report_id,
    filename: result.filename,
    media_type: result.media_type,
    created_at: null,
    verdict: null,
    authenticity_score: null,
    certainty: null,
    status: result.job_status,
    reasons: [],
    recommendations: [],
    segments: [],
    model_version: null,
  }
},

  feedback: async (_data: unknown): Promise<never> => {
    throw new Error('نموذج التقييم يحتاج ربطًا بمسار قرار الصحفي في الخادم.')
  },
}
