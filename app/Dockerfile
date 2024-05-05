FROM node:19-alpine

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install -g serve
RUN npm ci

RUN echo "REACT_APP_API_URL=https://group22.api.sprinty.tech" > .env

COPY . .

RUN npm run build
CMD [ "serve", "-s", "build" ]