import { api } from '../api'
import { useAsync } from '../hooks'
import { Badge, Card, Stat, State, fmtDate } from '../components/ui'

export default function Dashboard() {
  const s = useAsync(api.stats), r = useAsync(api.reports), h = useAsync(api.health)
  const days = ['س', 'ح', 'ن', 'ث', 'ر', 'خ', 'ج']
  const max = Math.max(1, ...(s.data?.weekly ?? [1]))
  return (
    <div className="grid">
      <State loading={s.loading} error={s.error}>
        {s.data && <>
          <div className="stats">
            <Stat label="إجمالي عمليات التحقق" value={s.data.total} />
            <Stat label="محتوى موثوق" value={s.data.authentic} tone="ok" />
            <Stat label="محتوى مشبوه" value={s.data.suspicious} tone="warn" />
            <Stat label="غير حاسمة" value={s.data.inconclusive} tone="mute" />
          </div>
          <Card title="نشاط التحليلات خلال الأسبوع">
            {s.data.weekly?.length ? <div className="bars">{s.data.weekly.map((v, i) =>
              <div key={i}><i style={{ height: `${(v / max) * 100}%` }} title={String(v)} /><small>{days[i]}</small></div>)}</div>
              : <p className="note">لا تتوفر بيانات أسبوعية من الـ API.</p>}
          </Card>
          <Card title="توزيع النتائج">
            <div className="dist">
              {([['authentic', 'ok'], ['suspicious', 'warn'], ['inconclusive', 'mute']] as const).map(([k, c]) =>
                <span key={k} className={c} style={{ flex: s.data![k] || 0.001 }} />)}
            </div>
          </Card>
        </>}
      </State>
      <Card title="أحدث التقارير / آخر الأنشطة">
        <State loading={r.loading} error={r.error} empty={!r.data?.length}>
          <ul className="list">{r.data?.slice(0, 5).map(x => (
            <li key={x.id}><a href={`#report/${x.id}`}>{x.filename}</a><Badge v={x.verdict} /><small>{fmtDate(x.created_at)}</small></li>))}</ul>
        </State>
      </Card>
      <Card title="حالة خدمة الذكاء الاصطناعي">
        <State loading={h.loading} error={h.error}><p><span className="dot ok" /> {h.data?.status ?? 'يعمل'}</p></State>
      </Card>
    </div>
  )
}
