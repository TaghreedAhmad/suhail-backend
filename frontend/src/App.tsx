import { useEffect, useState } from 'react'
import Dashboard from './pages/Dashboard'
import Analyze from './pages/Analyze'
import Reports from './pages/Reports'
import ReportPage from './pages/Report'
import Feedback from './pages/Feedback'

const NAV = [['dashboard', 'لوحة التحكم', '▦'], ['analyze', 'تحليل محتوى جديد', '⬆'], ['reports', 'جميع التقارير', '☰'],
  ['history', 'سجل التحليلات', '◷'], ['feedback', 'الملاحظات والتقييم', '✎'], ['settings', 'الإعدادات', '⚙']] as const

export default function App() {
  const [h, setH] = useState(location.hash.slice(1) || 'dashboard')
  useEffect(() => { const f = () => setH(location.hash.slice(1) || 'dashboard'); addEventListener('hashchange', f); return () => removeEventListener('hashchange', f) }, [])
  const [page, id] = h.split('/')
  const title = page === 'report' ? 'تقرير التحقق' : NAV.find(n => n[0] === page)?.[1] ?? ''
  const view = page === 'dashboard' ? <Dashboard /> : page === 'analyze' ? <Analyze /> : page === 'report' ? <ReportPage id={id} />
    : page === 'reports' || page === 'history' ? <Reports /> : page === 'feedback' ? <Feedback /> : <div className="state">قريباً.</div>
  return (
    <div className="app">
      <aside><div className="logo"><b>سُهيل</b><small>SUHAIL</small></div>
        <nav>{NAV.map(([k, l, i]) => <a key={k} href={`#${k}`} className={page === k ? 'on' : ''}><span>{i}</span>{l}</a>)}</nav>
        <p className="tag">تحقّق بذكاء، وانشر بثقة.</p></aside>
      <main><header><h1>{title}</h1><input placeholder="بحث…" /><button className="icon" aria-label="الإشعارات">🔔</button><span className="avatar">ص</span></header>
        <div className="content">{view}</div></main>
    </div>
  )
}
