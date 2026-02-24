import json
import threading
from http.client import HTTPConnection

from app import create_server


def _start_server():
    server = create_server(host="127.0.0.1", port=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


def _request(server, method, path, body=None):
    conn = HTTPConnection("127.0.0.1", server.server_port, timeout=2)
    headers = {"Content-Type": "application/json"}
    conn.request(method, path, body=body, headers=headers)
    response = conn.getresponse()
    raw = response.read().decode("utf-8")
    conn.close()
    return response.status, json.loads(raw)


def test_home_lists_endpoints():
    server, _ = _start_server()
    try:
        status, body = _request(server, "GET", "/")
        assert status == 200
        assert body["message"] == "Codex capability test app is running."
        assert "/health" in body["endpoints"]
    finally:
        server.shutdown()
        server.server_close()


def test_health_endpoint():
    server, _ = _start_server()
    try:
        status, body = _request(server, "GET", "/health")
        assert status == 200
        assert body == {"status": "ok"}
    finally:
        server.shutdown()
        server.server_close()


def test_echo_endpoint_round_trip_json():
    server, _ = _start_server()
    payload = {"prompt": "hello", "count": 3}
    try:
        status, body = _request(server, "POST", "/echo", body=json.dumps(payload))
        assert status == 200
        assert body == {"received": payload, "size": 2}
    finally:
        server.shutdown()
        server.server_close()
