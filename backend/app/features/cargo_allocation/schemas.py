from pydantic import BaseModel, Field


class CargoItem(BaseModel):
    id: str = Field(..., min_length=1)
    cubic_volume: float = Field(..., gt=0)


class TankerItem(BaseModel):
    id: str = Field(..., min_length=1)
    capacity: float = Field(..., gt=0)


class AllocationInputRequest(BaseModel):
    cargo: list[CargoItem] = Field(..., min_length=1)
    tankers: list[TankerItem] = Field(..., min_length=1)


class AllocationInputResponse(BaseModel):
    message: str
    cargo_count: int
    tanker_count: int


class AllocationItem(BaseModel):
    cargo_id: str
    tanker_id: str
    loaded_volume: float
    tanker_capacity: float
    unused_capacity: float


class UnallocatedCargoItem(BaseModel):
    cargo_id: str
    remaining_volume: float


class AllocationOptimizationResponse(BaseModel):
    message: str
    total_cargo_volume: float
    total_tanker_capacity: float
    total_loaded_volume: float
    total_unallocated_volume: float
    allocations: list[AllocationItem]
    unallocated_cargo: list[UnallocatedCargoItem]
