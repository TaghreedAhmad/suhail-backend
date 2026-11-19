import './App.css'

function App() {
  return (
    <div className="app" dir="rtl">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">س</div>
          <div>
            <h2>سُهيل</h2>
            <span>منصة التحقق الذكي</span>
          </div>
        </div>

        <nav>
          <p className="nav-label">القائمة الرئيسية</p>
          <a className="nav-item active" href="#">▦ لوحة التحكم</a>
          <a className="nav-item" href="#">＋ تحليل محتوى</a>
          <a className="nav-item" href="#">▤ التقارير</a>
          <a className="nav-item" href="#">◷ سجل التحليلات</a>

          <p className="nav-label">الإعدادات</p>
          <a className="nav-item" href="#">⚙ الإعدادات</a>
        </nav>

        <div className="sidebar-footer">
          <div className="user-avatar">ص</div>
          <div>
            <strong>المستخدم</strong>
            <span>صحفي</span>
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <span className="breadcrumb">الرئيسية / لوحة التحكم</span>
            <h1>لوحة التحكم</h1>
          </div>
          <div className="status">
            <span className="status-dot"></span>
            النظام جاهز
          </div>
        </header>

        <section className="welcome">
          <div>
            <span className="eyebrow">منصة سهيل للتحقق الإعلامي</span>
            <h2>مرحباً بك في سهيل 👋</h2>
            <p>
              تحقّق من المحتوى الإعلامي، وافهم مؤشرات المصداقية
              قبل اتخاذ قرار النشر.
            </p>
            <button className="primary-button">
              ＋ ابدأ تحليل محتوى
            </button>
          </div>
          <div className="welcome-symbol">س</div>
        </section>

        <section className="stats">
          <div className="stat-card">
            <span>إجمالي التقارير</span>
            <strong>0</strong>
            <small>جميع عمليات التحليل</small>
          </div>
          <div className="stat-card">
            <span>محتوى موثوق</span>
            <strong>0</strong>
            <small>نتائج موثوق بها</small>
          </div>
          <div className="stat-card">
            <span>محتوى مشبوه</span>
            <strong>0</strong>
            <small>يحتاج إلى مراجعة</small>
          </div>
          <div className="stat-card">
            <span>قيد التحليل</span>
            <strong>0</strong>
            <small>عمليات جارية</small>
          </div>
        </section>

        <section className="reports-section">
          <div className="section-heading">
            <div>
              <h2>أحدث التقارير</h2>
              <p>تابع نتائج عمليات التحقق الأخيرة</p>
            </div>
            <button className="secondary-button">عرض الكل</button>
          </div>

          <div className="empty-state">
            <div className="empty-icon">▤</div>
            <h3>لا توجد تقارير حتى الآن</h3>
            <p>ابدأ بتحليل أول ملف ليظهر تقرير التحقق هنا.</p>
          </div>
        </section>

        <footer className="footer">
          سهيل © 2026 — مساعدك الذكي للتحقق الإعلامي
        </footer>
      </main>
    </div>
  )
}

export default App