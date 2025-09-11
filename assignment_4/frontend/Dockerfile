FROM node:18-alpine

WORKDIR /app

COPY . .

# Installing npm
RUN npm install --production

EXPOSE 3000

CMD [ "node","server.js"]