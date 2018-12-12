const express = require('express')
const app = express()
const port = 3000
var amqp = require('amqplib');

app.get('/', (req, res) => {
  console.log("GET : Request received")

  amqp.connect({
  protocol: 'amqp',
  hostname: `${process.env.RABBITMQ_SERVER}`,
  port: 5672,
  username: 'srini',
  password: 'srini',
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

})

app.listen(port, () => console.log(`Example app listening on port ${port}!`))
