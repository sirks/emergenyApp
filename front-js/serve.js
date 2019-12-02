let connect = require('connect');
let serveStatic = require('serve-static');
let port = 3000;


connect().use(serveStatic(__dirname)).listen(port, () => console.log(`Server running on ${port}`));