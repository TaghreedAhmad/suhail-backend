
export type Verdict =
  | 'authentic'
  | 'suspicious'
  | 'inconclusive'
  | 'likely_fake'

export type Certainty = 'low' | 'medium' | 'high' | null

export interface Segment {
  start: number
  end: number
  note: string
}

export interface Report {
  id: string
  filename: string
  media_type: 'image' | 'video' | 'audio' | 'unknown'
  created_at: string | null
  verdict: Verdict | null
  authenticity_score: number | null
  certainty: Certainty
  status: string
  reasons: string[]
  recommendations: string[]
  segments: Segment[]
  model_version?: string | null
}

export interface Stats {
  total: number
  authentic: number
  suspicious: number
  inconclusive: number
  weekly: number[]
}
