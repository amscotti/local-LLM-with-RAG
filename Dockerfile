FROM python:3.11-slim

WORKDIR /app

# Установка необходимых зависимостей системы
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Копирование файлов зависимостей
COPY requirements.txt .

# Установка зависимостей Python
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода приложения
COPY . .

# Создание директории для документов, если она не существует
RUN mkdir -p Research

# Открытие портов для FastAPI и Streamlit
EXPOSE 8000 8501

# Команда для запуска FastAPI сервера и Streamlit
CMD ["bash", "-c", "uvicorn app:app --host 0.0.0.0 --port 8000 & streamlit run ui_client.py"] 