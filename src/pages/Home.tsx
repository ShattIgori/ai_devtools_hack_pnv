import React, { useState } from 'react'
import './Home.css'

const Home: React.FC = () => {
  const [requirements, setRequirements] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [selectedTemplate, setSelectedTemplate] = useState<string>('')

  const templates = [
    { id: 'auth', name: 'Авторизация', icon: '🔐', description: 'Шаблон для тестов авторизации' },
    { id: 'api', name: 'API Тесты', icon: '🌐', description: 'Тестирование REST API' },
    { id: 'ui', name: 'UI Тесты', icon: '🎨', description: 'Интерфейсные тесты' },
    { id: 'db', name: 'База данных', icon: '🗄️', description: 'Тесты базы данных' },
  ]

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!requirements.trim()) {
      alert('Введите требования')
      return
    }

    setIsLoading(true)
    setTimeout(() => {
      setIsLoading(false)
      alert('Требования успешно загружены и отправлены на обработку!')
      setRequirements('')
      setSelectedTemplate('')
    }, 2000)
  }

  const loadTemplate = (templateId: string) => {
    setSelectedTemplate(templateId)
    const templatesContent: Record<string, string> = {
      auth: `1. Пользователь должен иметь возможность зарегистрироваться с email и паролем
2. Email должен быть в правильном формате
3. Пароль должен быть не менее 8 символов
4. После регистрации должно отправляться письмо подтверждения
5. Пользователь должен подтвердить email для активации аккаунта
6. При неверных данных должна показываться понятная ошибка
7. Сессия должна сохраняться при перезагрузке страницы
8. Должна быть возможность восстановления пароля
9. При успешной авторизации должен создаваться JWT токен
10. Токен должен обновляться каждые 24 часа`,
      api: `1. Все endpoints должны возвращать правильные HTTP статусы
2. POST запросы должны валидировать входные данные
3. GET запросы должны поддерживать пагинацию
4. PUT/PATCH запросы должны частично обновлять ресурсы
5. DELETE запросы должны возвращать 204 статус
6. API должно поддерживать версионирование
7. Должна быть реализована rate limiting
8. Все ответы должны быть в формате JSON
9. Должна быть документация Swagger/OpenAPI
10. Должна быть обработка ошибок с понятными сообщениями`,
      ui: `1. Интерфейс должен быть адаптивным
2. Все элементы должны иметь адекватные отступы
3. Цветовая схема должна соответствовать бренду
4. Шрифты должны быть читаемыми
5. Кнопки должны иметь hover и active состояния
6. Формы должны иметь валидацию
7. Загрузка данных должна отображаться спиннером
8. Должна быть навигация между страницами
9. Сообщения об ошибках должны быть понятными
10. Должна быть поддержка клавиатуры`,
      db: `1. Все таблицы должны иметь первичные ключи
2. Должны быть созданы индексы для частых запросов
3. Должны быть foreign keys для связей
4. Должна быть реализована миграция данных
5. Должны быть регулярные бэкапы
6. Должна быть репликация для отказоустойчивости
7. Запросы должны быть оптимизированы
8. Должна быть очистка устаревших данных
9. Должно быть логирование важных операций
10. Должна быть защита от SQL инъекций`
    }
    setRequirements(templatesContent[templateId] || '')
  }

  return (
    <div className="home-page fade-in">
      <div className="page-header">
        <h1 className="page-title">Загрузка требований</h1>
        <p className="page-subtitle">Опишите технические требования для автоматического создания тестов</p>
      </div>

      <div className="grid-2">
        <div className="card">
          <div className="card-header">
            <h2 className="section-title">
              <span className="title-icon">📝</span>
              Введите требования
            </h2>
            <div className="card-actions">
              <button 
                className="btn btn-secondary btn-small"
                onClick={() => setRequirements('')}
                disabled={!requirements.trim() || isLoading}
              >
                Очистить
              </button>
            </div>
          </div>

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label className="form-label">
                Технические требования:
                <span className="char-count">
                  {requirements.length} символов
                </span>
              </label>
              <textarea
                className="form-textarea"
                placeholder="Введите требования построчно...
Пример:
1. Пользователь должен иметь возможность зарегистрироваться
2. Система должна проверять email на валидность
3. Пароль должен содержать минимум 8 символов
4. ..."
                value={requirements}
                onChange={(e) => setRequirements(e.target.value)}
                rows={18}
                disabled={isLoading}
              />
            </div>

            <div className="form-actions">
              <button
                type="submit"
                className="btn btn-primary"
                disabled={isLoading || !requirements.trim()}
              >
                {isLoading ? (
                  <>
                    <span className="spinner"></span>
                    Обработка...
                  </>
                ) : (
                  <>
                    <span className="btn-icon">🚀</span>
                    Сгенерировать тесты
                  </>
                )}
              </button>
              <div className="hint">
                Система автоматически создаст тест-кейсы на основе требований
              </div>
            </div>
          </form>
        </div>

        <div className="sidebar">
          <div className="card">
            <h2 className="section-title">
              <span className="title-icon">📋</span>
              Шаблоны требований
            </h2>
            <p className="card-description">
              Выберите шаблон для быстрого старта:
            </p>

            <div className="templates-grid">
              {templates.map((template) => (
                <div
                  key={template.id}
                  className={`template-card ${selectedTemplate === template.id ? 'selected' : ''}`}
                  onClick={() => loadTemplate(template.id)}
                >
                  <div className="template-icon">{template.icon}</div>
                  <div className="template-content">
                    <h4>{template.name}</h4>
                    <p>{template.description}</p>
                  </div>
                  <div className="template-badge">
                    {selectedTemplate === template.id ? '✓' : '→'}
                  </div>
                </div>
              ))}
            </div>

            <div className="stats-card">
              <h3>Статистика</h3>
              <div className="stats-grid">
                <div className="stat-item">
                  <div className="stat-value">12</div>
                  <div className="stat-label">Загружено</div>
                </div>
                <div className="stat-item">
                  <div className="stat-value">89%</div>
                  <div className="stat-label">Успешно</div>
                </div>
                <div className="stat-item">
                  <div className="stat-value">45</div>
                  <div className="stat-label">Тестов создано</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="card mt-4">
        <h2 className="section-title">
          <span className="title-icon">📊</span>
          Последние операции
        </h2>
        <div className="recent-activity">
          <div className="activity-item">
            <div className="activity-icon success">✓</div>
            <div className="activity-content">
              <div className="activity-title">Загружены требования авторизации</div>
              <div className="activity-meta">Сегодня, 14:30 • Создано 8 тестов</div>
            </div>
            <div className="activity-actions">
              <button className="btn btn-outline btn-small">Просмотр</button>
            </div>
          </div>
          <div className="activity-item">
            <div className="activity-icon warning">⏳</div>
            <div className="activity-content">
              <div className="activity-title">Обработка API требований</div>
              <div className="activity-meta">Сегодня, 11:15 • В процессе</div>
            </div>
            <div className="activity-actions">
              <button className="btn btn-outline btn-small">Отменить</button>
            </div>
          </div>
          <div className="activity-item">
            <div className="activity-icon success">✓</div>
            <div className="activity-content">
              <div className="activity-title">Созданы UI тесты</div>
              <div className="activity-meta">Вчера, 16:45 • Создано 12 тестов</div>
            </div>
            <div className="activity-actions">
              <button className="btn btn-outline btn-small">Просмотр</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home
