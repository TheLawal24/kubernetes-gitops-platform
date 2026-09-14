import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify(
        application="Kubernetes GitOps Platform",
        environment=os.getenv("APP_ENV", "unknown"),
        version=os.getenv("APP_VERSION", "dev"),
        message=os.getenv("APP_MESSAGE", "Hello from GKE")
    )

@app.route("/health")
def health():
    return jsonify(status="healthy"), 200

@app.route("/version")
def version():
    return jsonify(
        version=os.getenv("APP_VERSION", "dev")
    ), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
