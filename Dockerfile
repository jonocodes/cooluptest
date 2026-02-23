FROM nginx:alpine

ARG GIT_COMMIT=unknown

COPY index.html /usr/share/nginx/html/index.html

# Inject commit hash into the HTML page
RUN sed -i "s/__GIT_COMMIT__/${GIT_COMMIT}/g" /usr/share/nginx/html/index.html

# Serve commit hash at /version.json for server-side checks (curl, scripts, etc.)
RUN echo "{\"commit\":\"${GIT_COMMIT}\"}" > /usr/share/nginx/html/version.json
