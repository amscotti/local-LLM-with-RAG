FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

# Вторая стадия - использование Nginx для раздачи статических файлов
FROM nginx:alpine

# Копирование собранных файлов из предыдущей стадии
COPY --from=build /app/dist /usr/share/nginx/html

# Копирование конфигурации Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]