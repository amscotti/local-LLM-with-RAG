#!/bin/bash

echo "Запуск приложения в Docker..."

# Проверка наличия Docker
if ! command -v docker &> /dev/null; then
    echo "Docker не установлен. Пожалуйста, установите Docker и попробуйте снова."
    exit 1
fi

# Проверка наличия Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose не установлен. Пожалуйста, установите Docker Compose и попробуйте снова."
    exit 1
fi

# Вывод информации о сетевых интерфейсах
echo "Информация о сетевых интерфейсах:"
ipconfig

# Остановка существующих контейнеров для чистого запуска
echo "Остановка существующих контейнеров..."
docker-compose down

# Запуск контейнеров
echo "Запуск контейнеров..."
docker-compose up -d

# Проверка статуса контейнеров
echo "Проверка статуса контейнеров..."
docker-compose ps

# Получение IP-адреса хост-машины
HOST_IP=$(ipconfig | grep -A 5 "Ethernet adapter" | grep "IPv4" | head -n 1 | awk '{print $NF}')
if [ -z "$HOST_IP" ]; then
    HOST_IP=$(ipconfig | grep -A 5 "Wireless LAN adapter" | grep "IPv4" | head -n 1 | awk '{print $NF}')
fi

if [ -z "$HOST_IP" ]; then
    echo "Не удалось определить IP-адрес. Используйте IP-адрес вашей машины вместо localhost."
else
    echo ""
    echo "Приложение запущено!"
    echo "Фронтенд доступен по адресу: http://$HOST_IP:8080"
    echo "API бэкенда доступен по адресу: http://$HOST_IP:8000"
    echo "Документация API доступна по адресу: http://$HOST_IP:8000/docs"
    echo "Ollama API доступен по адресу: http://$HOST_IP:11434"
fi

echo ""
echo "Для загрузки моделей Ollama выполните:"
echo "docker exec -it ollama_service bash"
echo "ollama pull ilyagusev/saiga_llama3:latest"
echo "ollama pull snowflake-arctic-embed2:latest"
echo ""
echo "Для остановки приложения выполните: ./stop.sh" 