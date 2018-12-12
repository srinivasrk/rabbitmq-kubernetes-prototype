const express = require('express')
const app = express()
const port = 3000
var amqp = require('amqplib');



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
        res.send('Hello World!')
      }, {noAck: false})
    });
  });
});
