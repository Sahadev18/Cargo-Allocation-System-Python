from app.features.cargo_allocation.schemas import (
    AllocationInputRequest,
    AllocationOptimizationResponse,
)

_current_allocation_input: AllocationInputRequest | None = None
_current_optimization_result: AllocationOptimizationResponse | None = None


def replace_allocation_input(payload: AllocationInputRequest) -> AllocationInputRequest:
    global _current_allocation_input, _current_optimization_result

    _current_allocation_input = payload
    _current_optimization_result = None
    return payload


def get_current_allocation_input() -> AllocationInputRequest | None:
    return _current_allocation_input


def replace_optimization_result(
    result: AllocationOptimizationResponse,
) -> AllocationOptimizationResponse:
    global _current_optimization_result

    _current_optimization_result = result
    return result


def get_current_optimization_result() -> AllocationOptimizationResponse | None:
    return _current_optimization_result


def reset_allocation_state() -> None:
    global _current_allocation_input, _current_optimization_result

    _current_allocation_input = None
    _current_optimization_result = None
