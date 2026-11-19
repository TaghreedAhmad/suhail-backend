import { useState } from 'react'
import { api } from '../api'
import { Card } from '../components/ui'

export default function Feedback() {
  const [s, setS] = useState({ decision: 'publish', minutes: 0, confidence: 3, helped: true, notes: '' })
  const [msg, setMsg] = useState('')
  const set = (k: string, v: unknown) => setS({ ...s, [k]: v })
  const submit = async () => { try { await api.feedback(s); setMsg('تم حفظ التقييم، شكراً لك.') } catch (e) { setMsg((e as Error).message) } }
  return (
    <Card className="form">
      <label>قرار الصحفي<select value={s.decision} onChange={e => set('decision', e.target.value)}><option value="publish">نشر</option><option value="hold">إيقاف النشر</option></select></label>
      <label>الوقت المستغرق (دقائق)<input type="number" min={0} value={s.minutes} onChange={e => set('minutes', +e.target.value)} /></label>
      <label>مستوى الثقة: {s.confidence}/5<input type="range" min={1} max={5} value={s.confidence} onChange={e => set('confidence', +e.target.value)} /></label>
      <label>هل ساعدك سُهيل؟<select value={String(s.helped)} onChange={e => set('helped', e.target.value === 'true')}><option value="true">نعم</option><option value="false">لا</option></select></label>
      <label>ملاحظات<textarea rows={4} value={s.notes} onChange={e => set('notes', e.target.value)} /></label>
      <button className="btn" onClick={submit}>حفظ التقييم</button>{msg && <p className="note">{msg}</p>}
    </Card>
  )
}
