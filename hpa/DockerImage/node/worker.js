const express = require('express')
const app = express()
const port = 3000
var amqp = require('amqplib');


function fibo(n) {
  if (n < 2)
     return 1;
  else   return fibo(n - 2) + fibo(n - 1);
}

amqp.connect({
  protocol: 'amqp',
  hostname: `rabbitmq-service`,
  port: 5672,
  username: 'guest',
  password: 'guest',
  locale: 'en_US',
  frameMax: 0,
  heartbeat: 0
}).then((conn) => {
  conn.createChannel().then((ch) => {
    ch.assertQueue('hpa-custom', {durable: true}).then((q) => {
      console.log(' [*] Waiting for logs. To exit press CTRL+C');

      ch.consume(q.queue, function(msg) {
        console.log(" [x] Received %s", msg.content.toString());
        fibo(30)
        process.exit()
      }, {noAck: false})
    });
  });
});
