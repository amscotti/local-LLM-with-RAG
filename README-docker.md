# Запуск приложения в Docker

Данный проект настроен для запуска в Docker-контейнерах с использованием Docker Compose. Ниже приведены инструкции по запуску и управлению приложением.

## Предварительные требования

1. Установленный Docker: [Инструкция по установке Docker](https://docs.docker.com/get-docker/)
2. Установленный Docker Compose: [Инструкция по установке Docker Compose](https://docs.docker.com/compose/install/)
3. Для использования GPU с Ollama: установленный NVIDIA Container Toolkit (для систем с NVIDIA GPU): [Инструкция по установке](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)

## Структура проекта

Проект включает следующие компоненты:
- **Backend**: FastAPI-приложение на Python
- **Frontend**: Vue.js приложение с Vite
- **Database**: MySQL база данных
- **Ollama**: Сервис для работы с LLM-моделями

## Запуск приложения

### Первый запуск

1. Клонируйте репозиторий:
```bash
git clone <url-репозитория>
cd <директория-проекта>
```

2. Запустите все контейнеры:
```bash
docker-compose up -d
```

3. Проверьте, что все контейнеры запущены:
```bash
docker-compose ps
```

### Загрузка моделей Ollama

После первого запуска необходимо загрузить нужные модели в Ollama:

```bash
# Подключитесь к контейнеру Ollama
docker exec -it ollama_service bash

# Загрузите нужные модели
ollama pull ilyagusev/saiga_llama3:latest
ollama pull snowflake-arctic-embed2:latest
```

## Управление приложением

### Остановка контейнеров
```bash
docker-compose stop
```

### Запуск остановленных контейнеров
```bash
docker-compose start
```

### Полная остановка и удаление контейнеров
```bash
docker-compose down
```

### Полная остановка и удаление контейнеров и томов (удалит все данные)
```bash
docker-compose down -v
```

### Просмотр логов
```bash
# Все логи
docker-compose logs

# Логи конкретного сервиса
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db
docker-compose logs ollama

# Следить за логами в реальном времени
docker-compose logs -f
```

## Доступ к приложению

После успешного запуска всех контейнеров:

- **Frontend**: доступен по адресу http://localhost:8080
- **Backend API**: доступен по адресу http://localhost:8000
- **API документация**: доступна по адресу http://localhost:8000/docs
- **Ollama API**: доступен по адресу http://localhost:11434

### Проблемы с доступом по localhost

Если приложение недоступно по адресу localhost, используйте IP-адрес вашей машины вместо localhost. Для определения IP-адреса:

#### В Windows:
1. Запустите командную строку (cmd)
2. Выполните команду `ipconfig`
3. Найдите строку "IPv4 Address" и используйте указанный IP-адрес

Или запустите скрипт `get_ip.bat`, который автоматически определит IP-адрес.

#### В Linux:
```bash
ip addr show | grep "inet " | grep -v 127.0.0.1
```

После определения IP-адреса используйте его вместо localhost:
- **Frontend**: http://ВАШ_IP:8080
- **Backend API**: http://ВАШ_IP:8000
- **API документация**: http://ВАШ_IP:8000/docs
- **Ollama API**: http://ВАШ_IP:11434

## Устранение неполадок

### Проблемы с подключением к базе данных
Если бэкенд не может подключиться к базе данных, убедитесь, что контейнер с MySQL запущен и работает корректно:
```bash
docker-compose logs db
```

### Проблемы с Ollama
Если возникают проблемы с Ollama, проверьте логи:
```bash
docker-compose logs ollama
```

Для систем с GPU убедитесь, что NVIDIA Container Toolkit установлен и настроен правильно.

### Проблемы с сетевыми настройками

Если вы не можете получить доступ к сервисам через localhost или IP-адрес:

1. Проверьте, что порты не заняты другими приложениями:
```bash
# Windows
netstat -ano | findstr :8000
netstat -ano | findstr :8080
netstat -ano | findstr :11434

# Linux
netstat -tulpn | grep 8000
netstat -tulpn | grep 8080
netstat -tulpn | grep 11434
```

2. Проверьте, что брандмауэр не блокирует соединения:
   - В Windows: Проверьте настройки брандмауэра Windows и разрешите входящие соединения для Docker
   - В Linux: Проверьте настройки ufw или iptables

3. Перезапустите Docker:
```bash
# Windows
Restart-Service docker

# Linux
sudo systemctl restart docker
```

4. Перезапустите отдельные сервисы:
```bash
docker-compose restart backend
docker-compose restart frontend
docker-compose restart db
docker-compose restart ollama
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