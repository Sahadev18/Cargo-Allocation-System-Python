from fastapi.testclient import TestClient

from app.features.cargo_allocation.store import (
    get_current_optimization_result,
    reset_allocation_state,
)
from app.main import app

client = TestClient(app)


def test_optimize_returns_error_when_input_is_missing() -> None:
    reset_allocation_state()

    response = client.post("/api/v1/cargo-allocation/optimize")

    assert response.status_code == 400
    assert response.json() == {
        "detail": "No allocation input found. Upload cargo and tanker data first."
    }


def test_optimize_splits_cargo_across_tankers() -> None:
    reset_allocation_state()

    client.post(
        "/api/v1/cargo-allocation/input",
        json={
            "cargo": [{"id": "cargo-1", "cubic_volume": 180}],
            "tankers": [
                {"id": "tanker-1", "capacity": 100},
                {"id": "tanker-2", "capacity": 100},
            ],
        },
    )

    response = client.post("/api/v1/cargo-allocation/optimize")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Allocation optimization completed",
        "total_cargo_volume": 180.0,
        "total_tanker_capacity": 200.0,
        "total_loaded_volume": 180.0,
        "total_unallocated_volume": 0.0,
        "allocations": [
            {
                "cargo_id": "cargo-1",
                "tanker_id": "tanker-1",
                "loaded_volume": 100.0,
                "tanker_capacity": 100.0,
                "unused_capacity": 0.0,
            },
            {
                "cargo_id": "cargo-1",
                "tanker_id": "tanker-2",
                "loaded_volume": 80.0,
                "tanker_capacity": 100.0,
                "unused_capacity": 20.0,
            },
        ],
        "unallocated_cargo": [],
    }


def test_optimize_keeps_each_tanker_to_one_cargo_id() -> None:
    reset_allocation_state()

    client.post(
        "/api/v1/cargo-allocation/input",
        json={
            "cargo": [
                {"id": "cargo-1", "cubic_volume": 120},
                {"id": "cargo-2", "cubic_volume": 80},
            ],
            "tankers": [
                {"id": "tanker-1", "capacity": 100},
                {"id": "tanker-2", "capacity": 100},
            ],
        },
    )

    response = client.post("/api/v1/cargo-allocation/optimize")
    stored_result = get_current_optimization_result()

    assert response.status_code == 200
    assert response.json()["total_loaded_volume"] == 120.0
    assert response.json()["total_unallocated_volume"] == 80.0
    assert response.json()["allocations"] == [
        {
            "cargo_id": "cargo-1",
            "tanker_id": "tanker-1",
            "loaded_volume": 100.0,
            "tanker_capacity": 100.0,
            "unused_capacity": 0.0,
        },
        {
            "cargo_id": "cargo-1",
            "tanker_id": "tanker-2",
            "loaded_volume": 20.0,
            "tanker_capacity": 100.0,
            "unused_capacity": 80.0,
        },
    ]
    assert response.json()["unallocated_cargo"] == [
        {"cargo_id": "cargo-2", "remaining_volume": 80.0}
    ]
    assert stored_result is not None
    assert stored_result.total_loaded_volume == 120
