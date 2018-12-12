FROM ubuntu:18.04

WORKDIR /app
COPY package*.json ./
RUN npm i

COPY . .
EXPOSE 3000

CMD ["node", "worker.js"]
