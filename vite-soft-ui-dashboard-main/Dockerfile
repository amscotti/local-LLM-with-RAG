FROM node:lts-alpine

WORKDIR /app

ADD . .

RUN yarn && yarn build
EXPOSE 8080
CMD ["yarn", "preview"]