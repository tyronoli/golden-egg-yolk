// Temporary placeholder so the frontend container starts in T-001.
// T-003 replaces this with the Vite + React + TypeScript app. Safe to delete then.
const http = require("http");

http
  .createServer((req, res) => {
    res.writeHead(200, { "Content-Type": "text/plain; charset=utf-8" });
    res.end("Golden Egg Yolk Cooperatives - frontend placeholder (replaced in T-003)\n");
  })
  .listen(5173, "0.0.0.0");
