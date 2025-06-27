FROM node:18-alpine as build

WORKDIR /app

# Копирование файлов зависимостей
COPY package*.json ./

# Установка зависимостей
RUN npm install

# Копирование исходного кода приложения
COPY . .

# Сборка приложения
RUN npm run build

# Этап запуска
FROM nginx:alpine

# Копирование собранного приложения из этапа сборки
COPY --from=build /app/dist /usr/share/nginx/html

# Копирование конфигурации nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Экспонирование порта
EXPOSE 80

# Команда для запуска nginx
CMD ["nginx", "-g", "daemon off;"] 