import React, { useState } from 'react'
import './Home.css'

const Home: React.FC = () => {
  const [requirements, setRequirements] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!requirements.trim()) {
      alert('Введите требования')
      return
    }

    setIsLoading(true)
    // Имитация загрузки
    setTimeout(() => {
      setIsLoading(false)
      alert('Требования успешно загружены!')
      setRequirements('')
    }, 1500)
  }

  return (
    <div className="home-page">
      <div className="header">
        <h1>Загрузка требований</h1>
        <p className="subtitle">Введите технические требования для создания тестов</p>
      </div>

      <div className="content-card">
        <form onSubmit={handleSubmit}>
          <div className="form-section">
            <label htmlFor="requirements" className="form-label">
              Текст требований:
            </label>
            <textarea
              id="requirements"
              className="requirements-input"
              placeholder="Пример: 
1. Пользователь должен иметь возможность зарегистрироваться с email и паролем
2. Система должна проверять формат email
3. После регистрации отправляется письмо подтверждения
4. ..."
              rows={15}
              value={requirements}
              onChange={(e) => setRequirements(e.target.value)}
            />
            <div className="char-count">
              {requirements.length} символов
            </div>
          </div>

          <div className="form-actions">
            <button
              type="button"
              className="btn btn-secondary"
              onClick={() => setRequirements('')}
              disabled={isLoading}
            >
              Очистить
            </button>
            <button
              type="submit"
              className="btn btn-primary"
              disabled={isLoading || !requirements.trim()}
            >
              {isLoading ? (
                <>
                  <span className="spinner"></span>
                  Загрузка...
                </>
              ) : (
                'Загрузить требования'
              )}
            </button>
          </div>
        </form>

        <div className="info-section">
          <h3>Примеры формата:</h3>
          <ul className="examples-list">
            <li>• Используйте нумерованные списки</li>
            <li>• Описывайте конкретные сценарии</li>
            <li>• Указывайте ожидаемые результаты</li>
            <li>• Можно вставлять JSON или XML структуры</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default Home