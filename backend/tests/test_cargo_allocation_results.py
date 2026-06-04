from fastapi.testclient import TestClient

from app.features.cargo_allocation.store import reset_allocation_state
from app.main import app

client = TestClient(app)


def test_results_returns_error_when_optimization_has_not_run() -> None:
    reset_allocation_state()

    response = client.get("/api/v1/cargo-allocation/results")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "No optimization result found. Run optimization first."
    }


def test_results_returns_latest_optimization_result() -> None:
    reset_allocation_state()

    client.post(
        "/api/v1/cargo-allocation/input",
        json={
            "cargo": [{"id": "cargo-1", "cubic_volume": 75}],
            "tankers": [{"id": "tanker-1", "capacity": 100}],
        },
    )
    optimization_response = client.post("/api/v1/cargo-allocation/optimize")

    response = client.get("/api/v1/cargo-allocation/results")

    assert response.status_code == 200
    assert response.json() == optimization_response.json()
