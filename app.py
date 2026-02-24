import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class TestAppHandler(BaseHTTPRequestHandler):
    def _send_json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/":
            self._send_json(
                {
                    "message": "Codex capability test app is running.",
                    "endpoints": ["/", "/health", "/echo"],
                }
            )
            return

        if self.path == "/health":
            self._send_json({"status": "ok"})
            return

        self._send_json({"error": "not found"}, status=404)

    def do_POST(self) -> None:
        if self.path != "/echo":
            self._send_json({"error": "not found"}, status=404)
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length) if content_length > 0 else b"{}"

        try:
            payload = json.loads(raw_body.decode("utf-8")) if raw_body else {}
        except json.JSONDecodeError:
            self._send_json({"error": "invalid json"}, status=400)
            return

        if not isinstance(payload, dict):
            self._send_json({"error": "json body must be an object"}, status=400)
            return

        self._send_json({"received": payload, "size": len(payload)})


def create_server(host: str = "0.0.0.0", port: int = 5000) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), TestAppHandler)


def run(host: str = "0.0.0.0", port: int = 5000) -> None:
    server = create_server(host=host, port=port)
    print(f"Server running on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
