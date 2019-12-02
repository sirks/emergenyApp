let connect = require('connect');
let serveStatic = require('serve-static');
let port = 3000;
let host = '0.0.0.0';


connect().use(serveStatic(__dirname)).listen(
  port,
  host,
  () => console.log(`Server running on ${host}:${port}`));