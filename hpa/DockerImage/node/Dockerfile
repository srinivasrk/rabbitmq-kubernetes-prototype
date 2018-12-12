FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y curl ca-certificates amqp-tools gnupg \
       --no-install-recommends

RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -

RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -

RUN apt install nodejs

WORKDIR /app
COPY package*.json ./
RUN npm i

COPY . .
EXPOSE 3000

CMD ["node", "worker.js"]
