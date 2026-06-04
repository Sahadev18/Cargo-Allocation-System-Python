from fastapi import APIRouter, HTTPException, status

from app.features.cargo_allocation.optimizer import optimize_allocation
from app.features.cargo_allocation.schemas import (
    AllocationInputRequest,
    AllocationInputResponse,
    AllocationOptimizationResponse,
)
from app.features.cargo_allocation.store import (
    get_current_allocation_input,
    get_current_optimization_result,
    replace_allocation_input,
    replace_optimization_result,
)

router = APIRouter()


@router.post(
    "/input",
    response_model=AllocationInputResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_allocation_input(payload: AllocationInputRequest) -> AllocationInputResponse:
    stored_input = replace_allocation_input(payload)

    return AllocationInputResponse(
        message="Allocation input stored",
        cargo_count=len(stored_input.cargo),
        tanker_count=len(stored_input.tankers),
    )


@router.post("/optimize", response_model=AllocationOptimizationResponse)
async def optimize_current_allocation_input() -> AllocationOptimizationResponse:
    current_input = get_current_allocation_input()

    if current_input is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No allocation input found. Upload cargo and tanker data first.",
        )

    result = optimize_allocation(current_input)
    return replace_optimization_result(result)


@router.get("/results", response_model=AllocationOptimizationResponse)
async def get_latest_optimization_results() -> AllocationOptimizationResponse:
    result = get_current_optimization_result()

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No optimization result found. Run optimization first.",
        )

    return result
