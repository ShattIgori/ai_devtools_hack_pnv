import React, { useState } from 'react'
import './Tests.css'

interface TestCase {
  id: number
  name: string
  description: string
  status: 'passed' | 'failed' | 'running' | 'pending'
  lastRun: string
  steps: number
}

const Tests: React.FC = () => {
  const [tests, setTests] = useState<TestCase[]>([
    { id: 1, name: 'Авторизация пользователя', description: 'Проверка входа с валидными учетными данными', status: 'passed', lastRun: '2024-01-15 14:30', steps: 5 },
    { id: 2, name: 'Создание нового заказа', description: 'Создание заказа с несколькими товарами', status: 'failed', lastRun: '2024-01-15 14:25', steps: 8 },
    { id: 3, name: 'Поиск по каталогу', description: 'Поиск товаров с фильтрацией', status: 'pending', lastRun: '2024-01-14 11:20', steps: 6 },
    { id: 4, name: 'Добавление в корзину', description: 'Добавление товара в корзину покупок', status: 'passed', lastRun: '2024-01-14 10:15', steps: 4 },
    { id: 5, name: 'Оформление покупки', description: 'Полный цикл покупки товара', status: 'running', lastRun: '2024-01-15 15:45', steps: 12 },
  ])

  const [filter, setFilter] = useState<'all' | 'passed' | 'failed' | 'pending'>('all')

  const filteredTests = tests.filter(test => 
    filter === 'all' ? true : test.status === filter
  )

  const runTest = (id: number) => {
    setTests(tests.map(test => 
      test.id === id ? { ...test, status: 'running' } : test
    ))
    
    setTimeout(() => {
      setTests(tests.map(test => 
        test.id === id ? { 
          ...test, 
          status: Math.random() > 0.5 ? 'passed' : 'failed',
          lastRun: new Date().toLocaleString('ru-RU') 
        } : test
      ))
    }, 2000)
  }

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

  return (
    <div className="tests-page">
      <div className="page-header">
        <div>
          <h1>Просмотр тестов</h1>
          <p className="page-subtitle">Всего тестов: {tests.length}</p>
        </div>
        <button className="btn btn-success">
          + Создать новый тест
        </button>
      </div>

      <div className="filters">
        <div className="filter-buttons">
          <button 
            className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
            onClick={() => setFilter('all')}
          >
            Все ({tests.length})
          </button>
          <button 
            className={`filter-btn ${filter === 'passed' ? 'active' : ''}`}
            onClick={() => setFilter('passed')}
          >
            ✅ Пройдены ({tests.filter(t => t.status === 'passed').length})
          </button>
          <button 
            className={`filter-btn ${filter === 'failed' ? 'active' : ''}`}
            onClick={() => setFilter('failed')}
          >
            ❌ Провалены ({tests.filter(t => t.status === 'failed').length})
          </button>
          <button 
            className={`filter-btn ${filter === 'pending' ? 'active' : ''}`}
            onClick={() => setFilter('pending')}
          >
            ⏳ Ожидают ({tests.filter(t => t.status === 'pending').length})
          </button>
        </div>
      </div>

      <div className="tests-grid">
        {filteredTests.map((test) => (
          <div key={test.id} className="test-card">
            <div className="test-header">
              <div className="test-title">
                <span className="test-icon">{getStatusIcon(test.status)}</span>
                <h3>{test.name}</h3>
              </div>
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
            
            <p className="test-description">{test.description}</p>
            
            <div className="test-meta">
              <div className="meta-item">
                <span className="meta-label">ID:</span>
                <span className="meta-value">#{test.id}</span>
              </div>
              <div className="meta-item">
                <span className="meta-label">Последний запуск:</span>
                <span className="meta-value">{test.lastRun}</span>
              </div>
              <div className="meta-item">
                <span className="meta-label">Шагов:</span>
                <span className="meta-value">{test.steps}</span>
              </div>
            </div>

            <div className="test-actions">
              <button 
                className="btn btn-primary"
                onClick={() => runTest(test.id)}
                disabled={test.status === 'running'}
              >
                {test.status === 'running' ? 'Запуск...' : 'Запустить тест'}
              </button>
              <button className="btn btn-outline">
                Подробнее
              </button>
              <button className="btn btn-outline">
                Редактировать
              </button>
            </div>
          </div>
        ))}
      </div>

      {filteredTests.length === 0 && (
        <div className="empty-state">
          <div className="empty-icon">📋</div>
          <h3>Тесты не найдены</h3>
          <p>Нет тестов с выбранным статусом</p>
        </div>
      )}
    </div>
  )
}

export default Tests