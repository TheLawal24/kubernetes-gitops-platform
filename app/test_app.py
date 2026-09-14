import os

os.environ["APP_ENV"] = "test"
os.environ["APP_VERSION"] = "test-version"
os.environ["APP_MESSAGE"] = "CI test"

from app import app


def test_health():
    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_version():
    client = app.test_client()
    response = client.get("/version")

    assert response.status_code == 200
    assert response.get_json()["version"] == "test-version"


def test_home():
    client = app.test_client()
    response = client.get("/")

    data = response.get_json()

    assert response.status_code == 200
    assert data["application"] == "Kubernetes GitOps Platform"
    assert data["environment"] == "test"
