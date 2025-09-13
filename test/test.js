const assert = require('assert');
const server = require('../index');
const http = require('http');

describe('ping', () => {
  after(() => server.close());
  it('should return ok true', (done) => {
    http.get('http://localhost:3000/ping', (res) => {
      let body = '';
      res.on('data', c => body += c);
      res.on('end', () => {
        const json = JSON.parse(body);
        assert.strictEqual(json.ok, true);
        done();
      });
    });
  });
});
