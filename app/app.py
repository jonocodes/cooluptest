import os
import socket
from datetime import datetime, timezone

from flask import Flask

app = Flask(__name__)

# These are baked in at build time via Docker build args
GIT_COMMIT = os.environ.get("GIT_COMMIT", "unknown")
IMAGE_NAME = os.environ.get("IMAGE_NAME", "unknown")
BUILD_DATE = os.environ.get("BUILD_DATE", "unknown")


@app.route("/")
def index():
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask + Caddy Production App</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: system-ui, -apple-system, sans-serif;
            background: #0f172a;
            color: #e2e8f0;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 2rem;
        }}
        .container {{
            max-width: 640px;
            width: 100%;
        }}
        h1 {{
            font-size: 1.8rem;
            margin-bottom: 1.5rem;
            color: #38bdf8;
        }}
        .card {{
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1rem;
        }}
        .card h2 {{
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: #94a3b8;
            margin-bottom: 1rem;
        }}
        .row {{
            display: flex;
            justify-content: space-between;
            padding: 0.5rem 0;
            border-bottom: 1px solid #334155;
        }}
        .row:last-child {{ border-bottom: none; }}
        .label {{ color: #94a3b8; }}
        .value {{
            font-family: "SF Mono", "Fira Code", monospace;
            color: #f1f5f9;
            text-align: right;
            word-break: break-all;
        }}
        .badge {{
            display: inline-block;
            background: #38bdf8;
            color: #0f172a;
            font-weight: 700;
            padding: 0.15rem 0.6rem;
            border-radius: 4px;
            font-size: 0.85rem;
        }}
        .status-ok {{
            color: #4ade80;
        }}
        footer {{
            text-align: center;
            margin-top: 1.5rem;
            color: #475569;
            font-size: 0.8rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Flask + Caddy <span class="badge">Production</span></h1>

        <div class="card">
            <h2>Docker Info</h2>
            <div class="row">
                <span class="label">Image</span>
                <span class="value">{IMAGE_NAME}</span>
            </div>
            <div class="row">
                <span class="label">Commit</span>
                <span class="value">{GIT_COMMIT[:12] if len(GIT_COMMIT) > 12 else GIT_COMMIT}</span>
            </div>
            <div class="row">
                <span class="label">Built</span>
                <span class="value">{BUILD_DATE}</span>
            </div>
        </div>

        <div class="card">
            <h2>Runtime Info</h2>
            <div class="row">
                <span class="label">Hostname</span>
                <span class="value">{socket.gethostname()}</span>
            </div>
            <div class="row">
                <span class="label">Server Time (UTC)</span>
                <span class="value">{datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}</span>
            </div>
            <div class="row">
                <span class="label">Python Flask</span>
                <span class="value status-ok">Running</span>
            </div>
            <div class="row">
                <span class="label">Reverse Proxy</span>
                <span class="value status-ok">Caddy</span>
            </div>
        </div>

        <footer>Served by Gunicorn behind Caddy</footer>
    </div>
</body>
</html>"""


@app.route("/healthz")
def health():
    return {"status": "ok"}
