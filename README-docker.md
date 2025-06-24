# Запуск проекта с использованием Docker

В этом документе описаны шаги для запуска проекта с использованием Docker и Docker Compose.

## Предварительные требования

- Установленный Docker
- Установленный Docker Compose

## Структура проекта

Проект состоит из трех основных компонентов:
1. **Backend** - FastAPI приложение (директория `server`)
2. **Frontend** - Vue.js приложение (директория `vite-soft-ui-dashboard-main`)
3. **Database** - MySQL база данных

## Запуск проекта

1. Клонируйте репозиторий:
```bash
git clone <URL репозитория>
cd <директория проекта>
```

2. Запустите контейнеры с помощью Docker Compose:
```bash
docker-compose up -d
```

3. После запуска, сервисы будут доступны по следующим адресам:
   - Frontend: http://localhost:80
   - Backend API: http://localhost:8000
   - Swagger документация API: http://localhost:8000/docs

## Остановка проекта

Для остановки контейнеров выполните:
```bash
docker-compose down
```

Для остановки контейнеров и удаления томов (данных базы данных):
```bash
docker-compose down -v
```

## Логи

Для просмотра логов выполните:
```bash
# Все сервисы
docker-compose logs

# Конкретный сервис
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db
```

## Переменные окружения

Переменные окружения указаны непосредственно в файле `docker-compose.yml`:

### Backend
- `DATABASE_URL` - строка подключения к базе данных
- `PORT` - порт для FastAPI
- `HOST` - хост для FastAPI
- `DEFAULT_LLM_MODEL` - модель LLM по умолчанию
- `DEFAULT_EMBEDDING_MODEL` - модель эмбеддингов по умолчанию
- `DOCUMENTS_PATH` - путь к документам

### Database
- `MYSQL_ROOT_PASSWORD` - пароль root пользователя MySQL
- `MYSQL_DATABASE` - имя базы данных

## Дополнительная информация

При необходимости внесения изменений в код, контейнеры будут автоматически обновлять приложение благодаря монтированию томов. 