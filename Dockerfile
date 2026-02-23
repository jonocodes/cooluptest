FROM caddy:alpine

ARG GIT_COMMIT=unknown

COPY Caddyfile /etc/caddy/Caddyfile
COPY index.html /srv/index.html

# Inject commit hash into the HTML page
RUN sed -i "s/__GIT_COMMIT__/${GIT_COMMIT}/g" /srv/index.html

# Serve commit hash at /version.json for server-side checks (curl, scripts, etc.)
RUN echo "{\"commit\":\"${GIT_COMMIT}\"}" > /srv/version.json
