import os
import hashlib
import socket
from datetime import datetime, timezone
from pathlib import Path

import docker
from flask import Flask

app = Flask(__name__)

# These are baked in at build time via Docker build args
GIT_COMMIT = os.environ.get("GIT_COMMIT", "unknown")
IMAGE_NAME = os.environ.get("IMAGE_NAME", "unknown")
BUILD_DATE = os.environ.get("BUILD_DATE", "unknown")


def get_container_id():
    """Get the current container ID from /proc/self/cgroup or hostname."""
    try:
        cgroup = Path("/proc/self/cgroup").read_text()
        for line in cgroup.strip().splitlines():
            if "docker" in line or "containerd" in line:
                return line.rstrip().split("/")[-1][:12]
    except Exception:
        pass
    # In many Docker setups the hostname IS the short container ID
    return socket.gethostname()


def get_docker_info():
    """Query the Docker daemon for image and container details."""
    info = {
        "container_id": get_container_id(),
        "image_id": "unavailable",
        "image_digest": "unavailable",
        "container_name": "unavailable",
    }
    try:
        client = docker.from_env()
        hostname = socket.gethostname()

        # Find our own container by matching hostname to short container ID
        for container in client.containers.list():
            if container.short_id.replace("sha256:", "").startswith(hostname[:12]):
                info["container_id"] = container.short_id
                info["container_name"] = container.name
                # Image info
                image = container.image
                info["image_id"] = image.short_id.replace("sha256:", "")
                if image.attrs.get("RepoDigests"):
                    info["image_digest"] = image.attrs["RepoDigests"][0].split("@")[-1][:19] + "…"
                break
        client.close()
    except Exception:
        pass
    return info


def get_env_table():
    """Return a curated set of environment variables relevant to Docker/deployment."""
    keys = [
        "GIT_COMMIT", "IMAGE_NAME", "BUILD_DATE",
        "HOSTNAME", "PATH",
        "PYTHONUNBUFFERED", "LANG",
        "HOME", "GUNICORN_CMD_ARGS",
    ]
    env = {}
    for k in keys:
        v = os.environ.get(k)
        if v is not None:
            env[k] = v
    return env


@app.route("/")
def index():
    dinfo = get_docker_info()
    env_vars = get_env_table()

    env_rows = ""
    for k, v in env_vars.items():
        display_v = v if len(v) <= 60 else v[:57] + "…"
        env_rows += f"""
            <div class="row">
                <span class="label">{k}</span>
                <span class="value">{display_v}</span>
            </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cool Up Test App</title>
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

        <h2>test value: v4</h2>
        
        <div class="card">
            <h2>Build Info</h2>
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
            <h2>Docker Info</h2>
            <div class="row">
                <span class="label">Container ID</span>
                <span class="value">{dinfo['container_id']}</span>
            </div>
            <div class="row">
                <span class="label">Container Name</span>
                <span class="value">{dinfo['container_name']}</span>
            </div>
            <div class="row">
                <span class="label">Image ID</span>
                <span class="value">{dinfo['image_id']}</span>
            </div>
            <div class="row">
                <span class="label">Image Digest</span>
                <span class="value">{dinfo['image_digest']}</span>
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

        <div class="card">
            <h2>Container Environment</h2>
            {env_rows}
        </div>

        <footer>Served by Gunicorn behind Caddy</footer>
    </div>
</body>
</html>"""


@app.route("/healthz")
def health():
    return {"status": "ok"}
