let port = 3000;
let host = '0.0.0.0';

const fs = require('fs');
const https = require('https');
const express = require('express');

const app = express();
app.use(express.static(__dirname));

const options = {
  key: fs.readFileSync('key.pem', 'utf8'),
  cert: fs.readFileSync('cert.pem', 'utf8'),
};
const server = https.createServer(options, app);

server.listen(port, host, () => console.log(`Server running on ${host}:${port}`));