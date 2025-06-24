# Используем официальный образ Python в качестве базового
FROM python:latest

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt 

# Копируем все остальные файлы приложения
COPY . .

# Открываем порт для FastAPI
EXPOSE 8000

# Указываем команду для запуска приложения
CMD ["uvicorn", "app:app", "--host", "127.0.0.1", "--port", "8000"]
