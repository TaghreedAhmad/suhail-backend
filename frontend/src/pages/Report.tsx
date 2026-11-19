import { api } from '../api'
import { useAsync } from '../hooks'
import { Badge, Card, Disclaimer, State, fmtDate } from '../components/ui'

export default function ReportPage({ id }: { id: string }) {
  const { data: r, loading, error } = useAsync(() => api.report(id), [id])
  return (
    <State loading={loading} error={error} empty={!r}>
      {r && <div className="grid">
        <Card><div className="head"><div><h2>{r.filename}</h2><small>{fmtDate(r.created_at)} · {r.status}</small></div><Badge v={r.verdict} /></div>
          <div className="stats">
            <div className="meter"><b>{r.authenticity_score}%</b><span>درجة المصداقية</span></div>
            <div className="meter"><b>{r.certainty}%</b><span>مستوى اليقين</span></div>
            <div className="meter"><b>{r.model_version ?? '—'}</b><span>إصدار النموذج</span></div>
          </div><Disclaimer /></Card>
        <Card title="أسباب النتيجة">{r.reasons?.length ? <ul>{r.reasons.map((x, i) => <li key={i}>{x}</li>)}</ul> : <p className="note">لا توجد أسباب مسجّلة.</p>}</Card>
        <Card title="التوصيات">{r.recommendations?.length ? <ul>{r.recommendations.map((x, i) => <li key={i}>{x}</li>)}</ul> : <p className="note">لا توجد توصيات.</p>}</Card>
        <Card title="المقاطع المشبوهة">{r.segments?.length ? <ul className="list">{r.segments.map((s, i) =>
          <li key={i}><b>{s.start}ث – {s.end}ث</b><span>{s.note}</span></li>)}</ul> : <p className="note">لا توجد مقاطع مشبوهة.</p>}</Card>
      </div>}
    </State>
  )
}
