import React, { useState } from 'react'
import './Tests.css'

interface TestCase {
  id: number
  name: string
  description: string
  category: string
  priority: 'high' | 'medium' | 'low'
  status: 'passed' | 'failed' | 'running' | 'pending'
  lastRun: string
  duration: string
  steps: number
  author: string
}

const Tests: React.FC = () => {
  const [tests, setTests] = useState<TestCase[]>([
    { id: 1, name: 'Авторизация пользователя', description: 'Проверка входа с валидными учетными данными', category: 'Auth', priority: 'high', status: 'passed', lastRun: '15.01.2024 14:30', duration: '45s', steps: 5, author: 'Женя' },
    { id: 2, name: 'Создание нового заказа', description: 'Создание заказа с несколькими товарами', category: 'E-commerce', priority: 'high', status: 'failed', lastRun: '15.01.2024 14:25', duration: '1m 20s', steps: 8, author: 'Анна' },
    { id: 3, name: 'Поиск по каталогу', description: 'Поиск товаров с фильтрацией', category: 'Search', priority: 'medium', status: 'pending', lastRun: '14.01.2024 11:20', duration: '30s', steps: 6, author: 'Иван' },
    { id: 4, name: 'Добавление в корзину', description: 'Добавление товара в корзину покупок', category: 'E-commerce', priority: 'medium', status: 'passed', lastRun: '14.01.2024 10:15', duration: '25s', steps: 4, author: 'Женя' },
    { id: 5, name: 'Оформление покупки', description: 'Полный цикл покупки товара', category: 'Payment', priority: 'high', status: 'running', lastRun: '15.01.2024 15:45', duration: '2m 10s', steps: 12, author: 'Анна' },
    { id: 6, name: 'Регистрация нового пользователя', description: 'Создание аккаунта с подтверждением email', category: 'Auth', priority: 'medium', status: 'passed', lastRun: '13.01.2024 16:30', duration: '50s', steps: 7, author: 'Иван' },
    { id: 7, name: 'Восстановление пароля', description: 'Процесс восстановления забытого пароля', category: 'Auth', priority: 'low', status: 'pending', lastRun: '12.01.2024 09:45', duration: '35s', steps: 5, author: 'Женя' },
    { id: 8, name: 'Просмотр истории заказов', description: 'Отображение истории предыдущих покупок', category: 'Profile', priority: 'low', status: 'passed', lastRun: '12.01.2024 14:20', duration: '20s', steps: 3, author: 'Анна' },
  ])

  const [filter, setFilter] = useState<'all' | 'passed' | 'failed' | 'pending' | 'running'>('all')
  const [categoryFilter, setCategoryFilter] = useState<string>('all')
  const [searchQuery, setSearchQuery] = useState('')
  const [sortBy, setSortBy] = useState<'name' | 'priority' | 'lastRun'>('lastRun')

  const categories = ['all', ...Array.from(new Set(tests.map(test => test.category)))]

  const filteredTests = tests
    .filter(test => {
      const statusMatch = filter === 'all' ? true : test.status === filter
      const categoryMatch = categoryFilter === 'all' ? true : test.category === categoryFilter
      const searchMatch = test.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         test.description.toLowerCase().includes(searchQuery.toLowerCase())
      return statusMatch && categoryMatch && searchMatch
    })
    .sort((a, b) => {
      if (sortBy === 'name') return a.name.localeCompare(b.name)
      if (sortBy === 'priority') {
        const priorityOrder = { high: 0, medium: 1, low: 2 }
        return priorityOrder[a.priority] - priorityOrder[b.priority]
      }
      return new Date(b.lastRun).getTime() - new Date(a.lastRun).getTime()
    })

  const getStatusIcon = (status: TestCase['status']) => {
    switch(status) {
      case 'passed': return '✅'
      case 'failed': return '❌'
      case 'running': return '🔄'
      case 'pending': return '⏳'
      default: return '📋'
    }
  }

  const getStatusColor = (status: TestCase['status']) => {
    switch(status) {
      case 'passed': return '#10b981'
      case 'failed': return '#ef4444'
      case 'running': return '#3b82f6'
      case 'pending': return '#f59e0b'
      default: return '#6b7280'
    }
  }

  const getPriorityColor = (priority: TestCase['priority']) => {
    switch(priority) {
      case 'high': return '#ef4444'
      case 'medium': return '#f59e0b'
      case 'low': return '#10b981'
      default: return '#6b7280'
    }
  }

  const runTest = (id: number) => {
    setTests(tests.map(test => 
      test.id === id ? { ...test, status: 'running' } : test
    ))
    
    setTimeout(() => {
      setTests(tests.map(test => 
        test.id === id ? { 
          ...test, 
          status: Math.random() > 0.3 ? 'passed' : 'failed',
          lastRun: new Date().toLocaleString('ru-RU'),
          duration: `${Math.floor(Math.random() * 60)}s`
        } : test
      ))
    }, 2000)
  }

  const runAllTests = () => {
    const pendingTests = tests.filter(t => t.status !== 'running')
    setTests(tests.map(test => 
      pendingTests.some(t => t.id === test.id) ? { ...test, status: 'running' } : test
    ))
    
    setTimeout(() => {
      setTests(tests.map(test => 
        pendingTests.some(t => t.id === test.id) ? { 
          ...test, 
          status: Math.random() > 0.2 ? 'passed' : 'failed',
          lastRun: new Date().toLocaleString('ru-RU'),
          duration: `${Math.floor(Math.random() * 60)}s`
        } : test
      ))
    }, 3000)
  }

  return (
    <div className="tests-page fade-in">
      <div className="page-header">
        <div>
          <h1 className="page-title">Просмотр тестов</h1>
          <p className="page-subtitle">Управление и выполнение тест-кейсов</p>
        </div>
        <div className="header-actions">
          <button className="btn btn-success" onClick={runAllTests}>
            <span className="btn-icon">🚀</span>
            Запустить все тесты
          </button>
          <button className="btn btn-primary">
            <span className="btn-icon">➕</span>
            Новый тест
          </button>
        </div>
      </div>

      <div className="card">
        <div className="filters-bar">
          <div className="search-box">
            <span className="search-icon">🔍</span>
            <input
              type="text"
              placeholder="Поиск тестов..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="search-input"
            />
          </div>

          <div className="filter-controls">
            <select 
              value={categoryFilter}
              onChange={(e) => setCategoryFilter(e.target.value)}
              className="filter-select"
            >
              {categories.map(category => (
                <option key={category} value={category}>
                  {category === 'all' ? 'Все категории' : category}
                </option>
              ))}
            </select>

            <select 
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as any)}
              className="filter-select"
            >
              <option value="lastRun">Сортировка: Последний запуск</option>
              <option value="name">Сортировка: По имени</option>
              <option value="priority">Сортировка: По приоритету</option>
            </select>
          </div>
        </div>

        <div className="filter-tabs">
          <button 
            className={`filter-tab ${filter === 'all' ? 'active' : ''}`}
            onClick={() => setFilter('all')}
          >
            Все ({tests.length})
          </button>
          <button 
            className={`filter-tab ${filter === 'passed' ? 'active' : ''}`}
            onClick={() => setFilter('passed')}
          >
            ✅ Пройдены ({tests.filter(t => t.status === 'passed').length})
          </button>
          <button 
            className={`filter-tab ${filter === 'failed' ? 'active' : ''}`}
            onClick={() => setFilter('failed')}
          >
            ❌ Провалены ({tests.filter(t => t.status === 'failed').length})
          </button>
          <button 
            className={`filter-tab ${filter === 'running' ? 'active' : ''}`}
            onClick={() => setFilter('running')}
          >
            🔄 Выполняются ({tests.filter(t => t.status === 'running').length})
          </button>
          <button 
            className={`filter-tab ${filter === 'pending' ? 'active' : ''}`}
            onClick={() => setFilter('pending')}
          >
            ⏳ Ожидают ({tests.filter(t => t.status === 'pending').length})
          </button>
        </div>
      </div>

      <div className="stats-cards grid-4">
        <div className="stat-card success">
          <div className="stat-icon">✅</div>
          <div className="stat-content">
            <div className="stat-value">{tests.filter(t => t.status === 'passed').length}</div>
            <div className="stat-label">Пройдено</div>
          </div>
        </div>
        <div className="stat-card danger">
          <div className="stat-icon">❌</div>
          <div className="stat-content">
            <div className="stat-value">{tests.filter(t => t.status === 'failed').length}</div>
            <div className="stat-label">Провалено</div>
          </div>
        </div>
        <div className="stat-card warning">
          <div className="stat-icon">⏳</div>
          <div className="stat-content">
            <div className="stat-value">{tests.filter(t => t.status === 'pending').length}</div>
            <div className="stat-label">Ожидают</div>
          </div>
        </div>
        <div className="stat-card info">
          <div className="stat-icon">⏱️</div>
          <div className="stat-content">
            <div className="stat-value">{tests.length}</div>
            <div className="stat-label">Всего тестов</div>
          </div>
        </div>
      </div>

      <div className="tests-table-container">
        <div className="table-responsive">
          <table className="tests-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Название теста</th>
                <th>Категория</th>
                <th>Приоритет</th>
                <th>Статус</th>
                <th>Последний запуск</th>
                <th>Длительность</th>
                <th>Автор</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody>
              {filteredTests.map((test) => (
                <tr key={test.id}>
                  <td>
                    <div className="test-id">#{test.id}</div>
                  </td>
                  <td>
                    <div className="test-name">
                      <div className="test-title">{test.name}</div>
                      <div className="test-description">{test.description}</div>
                    </div>
                  </td>
                  <td>
                    <span className="category-badge">{test.category}</span>
                  </td>
                  <td>
                    <span 
                      className="priority-badge"
                      style={{ backgroundColor: getPriorityColor(test.priority) }}
                    >
                      {test.priority === 'high' && 'Высокий'}
                      {test.priority === 'medium' && 'Средний'}
                      {test.priority === 'low' && 'Низкий'}
                    </span>
                  </td>
                  <td>
                    <div className="status-cell">
                      <span className="status-icon">{getStatusIcon(test.status)}</span>
                      <span 
                        className="status-badge"
                        style={{ backgroundColor: getStatusColor(test.status) }}
                      >
                        {test.status === 'passed' && 'Пройден'}
                        {test.status === 'failed' && 'Провален'}
                        {test.status === 'running' && 'Выполняется'}
                        {test.status === 'pending' && 'Ожидает'}
                      </span>
                    </div>
                  </td>
                  <td>
                    <div className="last-run">{test.lastRun}</div>
                  </td>
                  <td>
                    <div className="duration">{test.duration}</div>
                  </td>
                  <td>
                    <div className="author">
                      <div className="author-avatar">{test.author.charAt(0)}</div>
                      <span>{test.author}</span>
                    </div>
                  </td>
                  <td>
                    <div className="action-buttons">
                      <button 
                        className="btn btn-primary btn-small"
                        onClick={() => runTest(test.id)}
                        disabled={test.status === 'running'}
                      >
                        {test.status === 'running' ? 'Запуск...' : 'Запустить'}
                      </button>
                      <button className="btn btn-outline btn-small">
                        Подробнее
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {filteredTests.length === 0 && (
          <div className="empty-state">
            <div className="empty-icon">🔍</div>
            <h3>Тесты не найдены</h3>
            <p>Попробуйте изменить параметры фильтрации</p>
          </div>
        )}
      </div>

      <div className="pagination">
        <button className="pagination-btn" disabled>←</button>
        <button className="pagination-btn active">1</button>
        <button className="pagination-btn">2</button>
        <button className="pagination-btn">3</button>
        <span className="pagination-ellipsis">...</span>
        <button className="pagination-btn">10</button>
        <button className="pagination-btn">→</button>
      </div>
    </div>
  )
}

export default Tests
