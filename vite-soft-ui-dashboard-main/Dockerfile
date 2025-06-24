# Этап сборки
FROM node:18-alpine as build-stage
COPY package*.json ./
RUN npm install crypto-browserify
RUN npm install
COPY . .
RUN npm run build

