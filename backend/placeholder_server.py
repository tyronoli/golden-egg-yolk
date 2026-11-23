"""Temporary placeholder so the backend container starts in T-001.

It only checks that Postgres and Redis are reachable on the Docker network.
T-002 replaces this file with the Django project. Safe to delete then.
"""
import json
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer


def reachable(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=2):
            return True
    except OSError:
        return False


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        body = json.dumps(
            {
                "service": "backend-placeholder",
                "postgres_reachable": reachable("db", 5432),
                "redis_reachable": reachable("redis", 6379),
            }
        ).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
