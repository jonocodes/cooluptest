# Coolify Deploy Test

A minimal Docker app for verifying that your [Coolify](https://coolify.io/) deployment pipeline is working. Push a change, watch Coolify redeploy, and confirm the new version is live by checking the commit hash on the page.

## How it works

The repo contains a single static HTML page served by [Caddy](https://caddyserver.com/) inside a lightweight Alpine container.

During the Docker build the current Git commit SHA is injected into:

- **the web page** — visible in the browser so you can eyeball which version is deployed
- **`/version.json`** — a JSON endpoint (`{"commit":"<sha>"}`) you can `curl` from scripts or health checks

## Quick start

```bash
# Build and run locally
GIT_COMMIT=$(git rev-parse HEAD) docker compose up --build

# Then open http://localhost in your browser
```

## Project structure

```
├── Caddyfile            # Caddy config — serves static files on port 80
├── Dockerfile           # Builds a caddy:alpine image with the HTML page
├── docker-compose.yml   # Single "web" service, forwards port 80
├── index.html           # The deploy-test page (commit hash placeholder)
└── README.md
```

## Deployment with Coolify

1. Point Coolify at this repo and let it build the Dockerfile.
2. Make sure Coolify passes `GIT_COMMIT` as a build argument (most setups do this automatically).
3. Push a commit — Coolify rebuilds and redeploys the container.
4. Reload the page and confirm the commit hash updated.

## Verifying a deploy

**Browser** — open the app and look at the commit hash shown on the page.

**CLI** — hit the JSON endpoint:

```bash
curl -s https://your-app.example.com/version.json | jq .
# {"commit":"a1b2c3d..."}
```
