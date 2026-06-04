from fastapi.testclient import TestClient

from app.features.cargo_allocation.store import get_current_allocation_input, reset_allocation_state
from app.main import app

client = TestClient(app)


def test_upload_allocation_input() -> None:
    reset_allocation_state()

    response = client.post(
        "/api/v1/cargo-allocation/input",
        json={
            "cargo": [
                {"id": "cargo-1", "cubic_volume": 120.5},
                {"id": "cargo-2", "cubic_volume": 80},
            ],
            "tankers": [
                {"id": "tanker-1", "capacity": 250},
            ],
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "message": "Allocation input stored",
        "cargo_count": 2,
        "tanker_count": 1,
    }


def test_upload_allocation_input_replaces_existing_data() -> None:
    reset_allocation_state()

    client.post(
        "/api/v1/cargo-allocation/input",
        json={
            "cargo": [{"id": "old-cargo", "cubic_volume": 100}],
            "tankers": [{"id": "old-tanker", "capacity": 100}],
        },
    )

    response = client.post(
        "/api/v1/cargo-allocation/input",
        json={
            "cargo": [{"id": "new-cargo", "cubic_volume": 200}],
            "tankers": [
                {"id": "new-tanker-1", "capacity": 150},
                {"id": "new-tanker-2", "capacity": 175},
            ],
        },
    )

    stored_input = get_current_allocation_input()

    assert response.status_code == 201
    assert response.json() == {
        "message": "Allocation input stored",
        "cargo_count": 1,
        "tanker_count": 2,
    }
    assert stored_input is not None
    assert [cargo.id for cargo in stored_input.cargo] == ["new-cargo"]
    assert [tanker.id for tanker in stored_input.tankers] == ["new-tanker-1", "new-tanker-2"]
