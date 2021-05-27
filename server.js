'use strict';
// завантаження бібліотек
const fs = require('fs');
const http = require('http');
const WebSocket = require('ws');
//завантажуємо сторінку
const index = fs.readFileSync('index.html');
// Завантажуємо модуль для побудови графіку
const jsFile = fs.readFileSync('sm.js');
// На любий http запит віддаємо 200 та сторінку
const server = http.createServer((req, res) => {
  
  
  // на запит від клієнту
  switch (req.url) {
    // на запит модулю
    case "/sm.js" :
    // відправляємо модуль
    res.writeHead(200, {"Content-Type": "text/javascript"});
    res.write(jsFile);
    break;
    // на інші 
    default :
    //передаємо сторінку
      res.writeHead(200, {"Content-Type": "text/html"});
      res.write(index);
  }

  res.end();
});

// підключаємо на порт 8000
server.listen(8000, () => {
  console.log('Listen port 8000');
});

// Запускаємо веб сокет, передаємо в нього змінну hhtp server
const ws = new WebSocket.Server({ server });
// на подію on conection(коли отримує запит на сокет)
// отримуємо сокет conection, який має додаткові методи

ws.on('connection', (connection, req) => {
  // отримуємо remote adress
  // відправляємо клієнту отримані повідомлення
    const ip = req.socket.remoteAddress;
    console.log(`Connected ${ip}`);
    connection.on('message', message => {
      console.log('Received: ' + message);
      for (const client of ws.clients) {
        if (client.readyState !== WebSocket.OPEN) continue;
        //if (client === connection) continue;
        client.send(message);
        //якщо на сервер прийшов код команди на завантаження
        if (message ==123456){ 
        // завантажуємо лог файли та відсилаємо клієнту
        let fileContent = fs.readFileSync("log1.txt", "utf8");
        let fileContent2 = fs.readFileSync("log2.txt", "utf8");
        client.send(fileContent)
        client.send(fileContent2)
      }
      // в іншому випадку, кожен монітор по id зберігаємо в свій лог файл
      var arrr = JSON.parse(message);
      var idd = arrr.id;
      if (idd === 1){
        fs.writeFileSync("log1.txt",message)
      }
      if (idd === 2){
        fs.writeFileSync("log2.txt",message)
      }
      }
    });


  connection.on('close', () => {
  console.log(`Disconnected ${ip}`);
  
  });
});