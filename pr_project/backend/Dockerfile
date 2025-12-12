# Dockerfile для backend (Task 6)
# Используем slim-версию Python для уменьшения размера образа
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем все файлы проекта в контейнер
# Сначала копируем только requirements.txt, если он есть, для кэширования слоев
# В нашем случае, мы просто копируем все
COPY . /app

# Устанавливаем зависимости
# В реальном проекте здесь был бы pip install -r requirements.txt
# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Указываем, что приложение будет слушать порт 8000
EXPOSE 8000

# Команда для запуска Uvicorn
# Запускаем app.py, а не main.py, так как app.py содержит FastAPI приложение
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
