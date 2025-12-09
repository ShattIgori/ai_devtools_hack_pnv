import React, { useState } from 'react'
import './Settings.css'

interface ApiKey {
  id: number
  name: string
  service: string
  key: string
  lastUsed: string
  isActive: boolean
}

const Settings: React.FC = () => {
  const [apiKeys, setApiKeys] = useState<ApiKey[]>([
    { id: 1, name: 'OpenAI Production', service: 'OpenAI', key: 'sk-...xyz123', lastUsed: '2024-01-15', isActive: true },
    { id: 2, name: 'GitHub Token', service: 'GitHub', key: 'ghp_...abc456', lastUsed: '2024-01-10', isActive: true },
    { id: 3, name: 'Test Environment', service: 'Custom API', key: 'test_...789', lastUsed: '2024-01-05', isActive: false },
  ])

  const [newKey, setNewKey] = useState({
    name: '',
    service: '',
    key: ''
  })

  const [showKey, setShowKey] = useState<number | null>(null)

  const handleAddKey = () => {
    if (!newKey.name.trim() || !newKey.service.trim() || !newKey.key.trim()) {
      alert('Заполните все поля')
      return
    }

    const newApiKey: ApiKey = {
      id: apiKeys.length + 1,
      name: newKey.name,
      service: newKey.service,
      key: newKey.key,
      lastUsed: new Date().toISOString().split('T')[0],
      isActive: true
    }

    setApiKeys([...apiKeys, newApiKey])
    setNewKey({ name: '', service: '', key: '' })
  }

  const toggleKeyVisibility = (id: number) => {
    setShowKey(showKey === id ? null : id)
  }

  const toggleKeyStatus = (id: number) => {
    setApiKeys(apiKeys.map(key => 
      key.id === id ? { ...key, isActive: !key.isActive } : key
    ))
  }

  const deleteKey = (id: number) => {
    if (window.confirm('Удалить этот API ключ?')) {
      setApiKeys(apiKeys.filter(key => key.id !== id))
    }
  }

  const maskKey = (key: string) => {
    if (key.length <= 8) return '••••••••'
    return `${key.substring(0, 3)}•••${key.substring(key.length - 4)}`
  }

  return (
    <div className="settings-page">
      <div className="page-header">
        <h1>Настройки API ключей</h1>
        <p className="page-subtitle">Управление доступом к внешним API</p>
      </div>

      <div className="settings-grid">
        <div className="settings-card">
          <h2>Добавить новый API ключ</h2>
          
          <div className="form-group">
            <label htmlFor="keyName">Название ключа *</label>
            <input
              id="keyName"
              type="text"
              placeholder="Например: OpenAI Production Key"
              value={newKey.name}
              onChange={(e) => setNewKey({...newKey, name: e.target.value})}
              className="form-input"
            />
          </div>

          <div className="form-group">
            <label htmlFor="service">Сервис *</label>
            <select
              id="service"
              value={newKey.service}
              onChange={(e) => setNewKey({...newKey, service: e.target.value})}
              className="form-select"
            >
              <option value="">Выберите сервис</option>
              <option value="OpenAI">OpenAI</option>
              <option value="GitHub">GitHub</option>
              <option value="GitLab">GitLab</option>
              <option value="Jira">Jira</option>
              <option value="Custom API">Custom API</option>
              <option value="Other">Другой</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="apiKey">API ключ *</label>
            <div className="input-with-icon">
              <input
                id="apiKey"
                type="password"
                placeholder="Вставьте ваш API ключ"
                value={newKey.key}
                onChange={(e) => setNewKey({...newKey, key: e.target.value})}
                className="form-input"
              />
            </div>
            <small className="input-hint">
              Ключ будет зашифрован и безопасно сохранен
            </small>
          </div>

          <button 
            onClick={handleAddKey}
            className="btn btn-primary btn-block"
            disabled={!newKey.name || !newKey.service || !newKey.key}
          >
            Добавить ключ
          </button>
        </div>

        <div className="settings-card">
          <h2>Управление ключами</h2>
          <p className="card-subtitle">Активных ключей: {apiKeys.filter(k => k.isActive).length}</p>

          <div className="keys-list">
            {apiKeys.map((apiKey) => (
              <div key={apiKey.id} className="key-item">
                <div className="key-header">
                  <div className="key-info">
                    <h4>{apiKey.name}</h4>
                    <div className="key-tags">
                      <span className="service-tag">{apiKey.service}</span>
                      <span className={`status-tag ${apiKey.isActive ? 'active' : 'inactive'}`}>
                        {apiKey.isActive ? 'Активен' : 'Неактивен'}
                      </span>
                    </div>
                  </div>
                  <div className="key-actions">
                    <button 
                      className="icon-btn"
                      onClick={() => toggleKeyVisibility(apiKey.id)}
                      title="Показать/скрыть ключ"
                    >
                      👁️
                    </button>
                    <button 
                      className="icon-btn"
                      onClick={() => toggleKeyStatus(apiKey.id)}
                      title={apiKey.isActive ? 'Деактивировать' : 'Активировать'}
                    >
                      {apiKey.isActive ? '⚡' : '⏸️'}
                    </button>
                    <button 
                      className="icon-btn danger"
                      onClick={() => deleteKey(apiKey.id)}
                      title="Удалить"
                    >
                      🗑️
                    </button>
                  </div>
                </div>

                <div className="key-details">
                  <div className="key-value">
                    <span className="key-label">Ключ:</span>
                    <span className="key-text">
                      {showKey === apiKey.id ? apiKey.key : maskKey(apiKey.key)}
                    </span>
                  </div>
                  <div className="key-meta">
                    <span className="meta-item">
                      <span className="meta-label">ID:</span>
                      <span className="meta-value">#{apiKey.id}</span>
                    </span>
                    <span className="meta-item">
                      <span className="meta-label">Использован:</span>
                      <span className="meta-value">{apiKey.lastUsed}</span>
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {apiKeys.length === 0 && (
            <div className="empty-keys">
              <div className="empty-icon">🔑</div>
              <p>Нет сохраненных API ключей</p>
            </div>
          )}
        </div>
      </div>

      <div className="settings-card">
        <h2>Инструкция по безопасности</h2>
        <div className="security-tips">
          <div className="tip">
            <div className="tip-icon">🔒</div>
            <div className="tip-content">
              <h4>Никому не передавайте ключи</h4>
              <p>API ключи — это как пароли, храните их в секрете</p>
            </div>
          </div>
          <div className="tip">
            <div className="tip-icon">🔄</div>
            <div className="tip-content">
              <h4>Регулярно обновляйте ключи</h4>
              <p>Меняйте ключи каждые 3-6 месяцев</p>
            </div>
          </div>
          <div className="tip">
            <div className="tip-icon">👨‍💻</div>
            <div className="tip-content">
              <h4>Используйте разные ключи для окружений</h4>
              <p>Разделяйте ключи для development, staging и production</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Settings