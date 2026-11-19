import { useRef, useState } from 'react'
import { api } from '../api'
import { Card } from '../components/ui'

const OK = /^(image|video|audio)\//
export default function Analyze() {
  const [file, setFile] = useState<File | null>(null)
  const [url, setUrl] = useState('')
  const [pct, setPct] = useState(0)
  const [busy, setBusy] = useState(false)
  const [msg, setMsg] = useState('')
  const [drag, setDrag] = useState(false)
  const input = useRef<HTMLInputElement>(null)

  const pick = (f?: File) => {
    if (!f) return
    if (!OK.test(f.type)) return setMsg('نوع الملف غير مدعوم: صورة أو فيديو أو صوت فقط.')
    setMsg(''); setFile(f); setPct(0); setUrl(URL.createObjectURL(f))
  }
  const start = async () => {
    if (!file) return
    setBusy(true); setMsg('جارٍ الرفع والمعالجة…')
    try { const r = await api.analyze(file, setPct); location.hash = `report/${r.id}` }
    catch (e) { setMsg((e as Error).message) } finally { setBusy(false) }
  }
  const kind = file?.type.split('/')[0]
  return (
    <Card>
      <div className={`drop ${drag ? 'on' : ''}`} onClick={() => input.current?.click()}
        onDragOver={e => { e.preventDefault(); setDrag(true) }} onDragLeave={() => setDrag(false)}
        onDrop={e => { e.preventDefault(); setDrag(false); pick(e.dataTransfer.files[0]) }}>
        <b>اسحب الملف وأفلته هنا</b><span>صور · فيديو · تسجيلات صوتية</span>
        <button className="btn ghost" type="button">اختيار ملف</button>
        <input ref={input} type="file" hidden accept="image/*,video/*,audio/*" onChange={e => pick(e.target.files?.[0])} />
      </div>
      {file && <div className="file">
        {kind === 'image' && <img src={url} alt="" />}{kind === 'video' && <video src={url} controls />}{kind === 'audio' && <audio src={url} controls />}
        <div><b>{file.name}</b><small>{file.type} · {(file.size / 1048576).toFixed(2)} MB</small>
          {busy && <div className="prog"><i style={{ width: `${pct}%` }} /></div>}</div>
      </div>}
      {msg && <p className="note">{msg}</p>}
      <button className="btn" disabled={!file || busy} onClick={start}>{busy ? 'جارٍ التحليل…' : 'ابدأ التحليل'}</button>
    </Card>
  )
}
