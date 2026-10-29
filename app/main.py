import os
import time

from flask import Flask, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
START = time.time()

REQUESTS = Counter("myapi_requests_total", "Total requests", ["endpoint"])
LATENCY = Histogram("myapi_request_seconds", "Request latency", ["endpoint"])


@app.get("/")
def index():
    with LATENCY.labels("/").time():
        REQUESTS.labels("/").inc()
        return jsonify(
            message="Hello from myapi, deployed via Argo CD",
            version=os.getenv("APP_VERSION", "0.1.0"),
            pod=os.getenv("HOSTNAME", "unknown"),
        )


@app.get("/health")
def health():
    REQUESTS.labels("/health").inc()
    return jsonify(status="ok", uptime_seconds=round(time.time() - START, 1))


@app.get("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
