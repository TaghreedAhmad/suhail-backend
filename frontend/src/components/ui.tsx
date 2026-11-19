import type { ReactNode } from 'react'
import type { Verdict } from '../types'

export const VERDICT: Record<Verdict, { label: string; cls: string }> = {
  authentic: { label: 'موثوق', cls: 'ok' },
  suspicious: { label: 'مشبوه', cls: 'warn' },
  inconclusive: { label: 'غير حاسم', cls: 'mute' },
  likely_fake: { label: 'مرجّح التزييف', cls: 'bad' },
}

export const Badge = ({ v }: { v: Verdict | null }) => {
  const item = v ? VERDICT[v] : null
  return (
    <span className={`badge ${item?.cls ?? 'mute'}`}>
      {item?.label ?? 'غير محدد'}
    </span>
  )
}

export const Card = ({ title, children, className = '' }: {
  title?: string
  children: ReactNode
  className?: string
}) => (
  <section className={`card ${className}`}>
    {title && <h3>{title}</h3>}
    {children}
  </section>
)

export const Stat = ({ label, value, tone }: {
  label: string
  value: number | string
  tone?: string
}) => (
  <div className={`card stat ${tone ?? ''}`}>
    <span>{label}</span>
    <b>{value}</b>
  </div>
)

export function State({ loading, error, empty, children }: {
  loading: boolean
  error: string | null
  empty?: boolean
  children: ReactNode
}) {
  if (loading) return <div className="state"><div className="spin" />جارٍ التحميل…</div>
  if (error) return <div className="state err">⚠ {error}</div>
  if (empty) return <div className="state">لا توجد بيانات بعد.</div>
  return <>{children}</>
}

export const Disclaimer = () => (
  <p className="note">
    سُهيل أداة مساعدة، والنتيجة مؤشر احتمالي لا حكم قطعي، ولا تغني عن التحقق البشري.
  </p>
)

export const fmtDate = (s: string | null) =>
  s ? new Date(s).toLocaleDateString('ar', { dateStyle: 'medium' }) : 'غير متاح'
