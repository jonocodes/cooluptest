FROM python:3.12-slim

ARG GIT_COMMIT=unknown
ARG IMAGE_NAME=unknown
ARG BUILD_DATE=unknown

ENV GIT_COMMIT=${GIT_COMMIT}
ENV IMAGE_NAME=${IMAGE_NAME}
ENV BUILD_DATE=${BUILD_DATE}

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--access-logfile", "-", "app:app"]
