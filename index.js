const http = require('http');

const server = http.createServer((req, res) => {
  if (req.url === '/ping') return res.end(JSON.stringify({ ok: true }));
  res.statusCode = 404; res.end('not found');
});

server.listen(3000, () => console.log('listening'));
module.exports = server;
