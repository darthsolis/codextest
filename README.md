# codextest

A tiny dependency-free Python app to help you test Codex workflows quickly.

## What it does

- `GET /` returns a message and a list of available endpoints.
- `GET /health` returns a simple health check payload.
- `POST /echo` returns the JSON payload you send plus a key count.

## Quick start

```bash
python app.py
```

Then open `http://localhost:5000`.

## Run tests

```bash
python -m pytest
```
