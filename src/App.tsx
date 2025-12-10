import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom'
import Home from './pages/Home'
import Tests from './pages/Tests'
import Settings from './pages/Settings'
import './App.css'

const Navigation = () => {
  const location = useLocation()
  
  return (
    <nav className="navbar">
      <div className="nav-header">
        <Link to="/" className="app-logo">
          <span className="logo-icon">🧪</span>
          TestMaster Pro
        </Link>
        <div className="app-subtitle">Платформа для тестирования</div>
      </div>
      
      <div className="nav-menu">
        <Link 
          to="/" 
          className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}
        >
          <span className="nav-icon">📥</span>
          Загрузка требований
          <span className="nav-badge">Главная</span>
        </Link>
        
        <Link 
          to="/tests" 
          className={`nav-link ${location.pathname === '/tests' ? 'active' : ''}`}
        >
          <span className="nav-icon">🧪</span>
          Просмотр тестов
          <span className="nav-badge">12</span>
        </Link>
        
        <Link 
          to="/settings" 
          className={`nav-link ${location.pathname === '/settings' ? 'active' : ''}`}
        >
          <span className="nav-icon">⚙️</span>
          Настройки API
          <span className="nav-badge">3</span>
        </Link>
        
        <div className="nav-divider"></div>
        
        <div className="nav-footer">
          <div className="user-info">
            <div className="user-avatar">Ваш</div>
            <div>
              <div className="user-name">Помощник</div>
              <div className="user-role">В разработке</div>
            </div>
          </div>
        </div>
      </div>
    </nav>
  )
}

function App() {
  return (
    <Router>
      <div className="app">
        <Navigation />
        
        <main className="main-content">
          <div className="page-container">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/tests" element={<Tests />} />
              <Route path="/settings" element={<Settings />} />
            </Routes>
          </div>
        </main>
      </div>
    </Router>
  )
}

export default App
