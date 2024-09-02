# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем Poetry
RUN pip install poetry

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы pyproject.toml и poetry.lock для установки зависимостей
COPY pyproject.toml poetry.lock ./

# Копируем весь проект в контейнер
COPY . .

# Устанавливаем переменную окружения для Flask
ENV FLASK_APP=src/main.py

# Устанавливаем зависимости
RUN poetry config virtualenvs.create false && poetry install --only main

# Экспонируем порт 8083
EXPOSE 8083

# Команда для запуска Flask-приложения
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=8083"]
