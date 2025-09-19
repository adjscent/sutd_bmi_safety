// server.js
const { createServer } = require('http');
const next = require('next');
const socketio = require('socket.io');
const connect = require('./readSerial');
const findESP32Port = require('./findSerial');

const dev = process.env.NODE_ENV !== 'production';
const app = next({ dev });
const handle = app.getRequestHandler();

const TEST_MODE = process.env.TEST_MODE === 'true';
const SAMPLE_RATE = +process.env.SAMPLE_RATE || 100;
const HTTP_PORT = +process.env.HTTP_PORT || 3000;


var SERIAL_PORT = process.env.SERIAL_PORT;

if (!SERIAL_PORT) {
  findESP32Port().then((port) => {
    SERIAL_PORT = port;
  })
}

app.prepare().then(() => {
  const server = createServer((req, res) => handle(req, res));
  const io = socketio(server, { cors: { origin: '*' } });

  io.on('connection', (socket) => {
    console.log('Client connected:', socket.id);
  });

  if (TEST_MODE) {
    console.log('TEST MODE emitting random data');
    setInterval(() => {
      const mk = () => Math.floor(Math.random()*2047)-1023;
      io.emit('adc_data', {
        ch0: { a: mk(), e: mk() },
        ch1: { a: mk(), e: mk() },
      });
    }, 1000 / SAMPLE_RATE);
  } else {
    console.log('Reading from serial port');
    connect(io, SERIAL_PORT, SAMPLE_RATE);
  }

  server.listen(HTTP_PORT, () => {
    console.log(`> Ready on http://localhost:${HTTP_PORT}`);
  });
});
