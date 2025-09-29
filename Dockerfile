FROM python:3.11-slim-bullseye

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копирование файлов зависимостей
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY bot.py .

# Создание пользователя для безопасности
RUN useradd --create-home --shell /bin/bash botuser
USER botuser

# Команда запуска
CMD ["python", "bot.py"]
