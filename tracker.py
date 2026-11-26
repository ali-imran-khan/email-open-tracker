import base64
import os
from datetime import datetime

import requests
from flask import Flask, request

app = Flask(__name__)

# 1x1 transparent png
PIXEL = base64.b64decode(
    b"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "opens.log")
WEBHOOK_URL = os.environ.get("N8N_WEBHOOK_URL", "")


@app.route("/track.png")
def track_open():
    recipient = request.args.get("id", "unknown")
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a") as f:
        f.write(f"[{ts}] opened by: {recipient}\n")

    if WEBHOOK_URL:
        try:
            requests.post(WEBHOOK_URL, json={"prospect": recipient, "timestamp": ts}, timeout=5)
        except requests.exceptions.RequestException as e:
            # n8n being down shouldn't break the pixel
            print(f"webhook failed: {e}")

    resp = app.response_class(PIXEL, mimetype="image/png")
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    return resp


if __name__ == "__main__":
    # PythonAnywhere runs the app through WSGI, this is just for local testing
    app.run(host="0.0.0.0", port=5000)
