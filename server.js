const http = require("http");
const fs   = require("fs");
const path = require("path");

const PORT = 3000;

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".css" : "text/css",
  ".js"  : "text/javascript",
  ".png" : "image/png",
  ".jpg" : "image/jpeg",
  ".jpeg": "image/jpeg",
  ".svg" : "image/svg+xml",
  ".ico" : "image/x-icon",
  ".woff2": "font/woff2",
};

const server = http.createServer((req, res) => {
  let url = req.url === "/" ? "/index.html" : req.url;
  // Remove query strings
  url = url.split("?")[0];
  
  const filePath = path.join(__dirname, url);
  const ext      = path.extname(filePath).toLowerCase();
  const mime     = MIME[ext] || "application/octet-stream";

  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404, { "Content-Type": "text/plain" });
      res.end("404 — Arquivo nao encontrado: " + url);
      return;
    }
    res.writeHead(200, { "Content-Type": mime });
    res.end(data);
  });
});

server.listen(PORT, () => {
  console.log("\\n  🖤  Slow Flow Studio — Servidor local");
  console.log("  ➜  http://localhost:" + PORT);
  console.log("  ➜  Pressione Ctrl+C para parar\\n");
});

