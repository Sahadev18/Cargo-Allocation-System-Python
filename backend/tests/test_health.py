from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_api_base() -> None:
    response = client.get("/api/v1")

    assert response.status_code == 200
    assert response.json() == {
        "name": "Cargo Allocation API",
        "version": "v1",
        "status": "ready",
    }


def test_root_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_api_health() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
