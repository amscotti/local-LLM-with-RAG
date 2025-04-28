# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт, на котором будет работать приложение
EXPOSE 8000

# Запускаем приложение
CMD ["streamlit", "run", "ui_client.py", "--server.port=8000", "--server.address=0.0.0.0"]