import { useMemo, useState } from 'react'
import { api } from '../api'
import { useAsync } from '../hooks'
import { Badge, Card, State, VERDICT, fmtDate } from '../components/ui'
import type { Verdict } from '../types'

export default function Reports() {
  const { data, loading, error } = useAsync(api.reports)
  const [q, setQ] = useState(''), [f, setF] = useState(''), [asc, setAsc] = useState(false)
  const rows = useMemo(() => (data ?? [])
    .filter(r => (!f || r.verdict === f) && r.filename.toLowerCase().includes(q.toLowerCase()))
    .sort((a, b) => (asc ? 1 : -1) * ((a.created_at ? new Date(a.created_at).getTime() : 0) - (b.created_at ? new Date(b.created_at).getTime() : 0))), [data, q, f, asc])
  return (
    <Card>
      <div className="tools">
        <input placeholder="ابحث باسم الملف…" value={q} onChange={e => setQ(e.target.value)} />
        <select value={f} onChange={e => setF(e.target.value)}><option value="">كل النتائج</option>
          {(Object.keys(VERDICT) as Verdict[]).map(k => <option key={k} value={k}>{VERDICT[k].label}</option>)}</select>
        <button className="btn ghost" onClick={() => setAsc(!asc)}>التاريخ {asc ? '↑' : '↓'}</button>
      </div>
      <State loading={loading} error={error} empty={!rows.length}>
        <div className="scroll"><table><thead><tr><th>الرقم</th><th>الملف</th><th>النوع</th><th>التاريخ</th><th>النتيجة</th><th>المصداقية</th><th>الحالة</th><th /></tr></thead>
          <tbody>{rows.map(r => <tr key={r.id}><td>{r.id}</td><td>{r.filename}</td><td>{r.media_type}</td><td>{fmtDate(r.created_at)}</td>
            <td><Badge v={r.verdict} /></td><td>{r.authenticity_score}%</td><td>{r.status}</td><td><a className="btn ghost" href={`#report/${r.id}`}>عرض</a></td></tr>)}</tbody></table></div>
      </State>
    </Card>
  )
}
