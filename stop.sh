#!/bin/bash

echo "Остановка приложения в Docker..."

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

# Остановка контейнеров
echo "Остановка контейнеров..."
docker-compose stop

echo ""
echo "Приложение остановлено!"
echo ""
echo "Для полного удаления контейнеров выполните: docker-compose down"
echo "Для полного удаления контейнеров и томов (данных) выполните: docker-compose down -v"
echo "Для запуска приложения выполните: ./start.sh" 