from app.features.cargo_allocation.schemas import (
    AllocationInputRequest,
    AllocationItem,
    AllocationOptimizationResponse,
    UnallocatedCargoItem,
)


def optimize_allocation(payload: AllocationInputRequest) -> AllocationOptimizationResponse:
    allocations: list[AllocationItem] = []
    unallocated_cargo: list[UnallocatedCargoItem] = []
    cargo_index = 0
    remaining_cargo_volume = payload.cargo[cargo_index].cubic_volume

    for tanker in payload.tankers:
        if cargo_index >= len(payload.cargo):
            break

        current_cargo = payload.cargo[cargo_index]
        loaded_volume = min(remaining_cargo_volume, tanker.capacity)

        allocations.append(
            AllocationItem(
                cargo_id=current_cargo.id,
                tanker_id=tanker.id,
                loaded_volume=loaded_volume,
                tanker_capacity=tanker.capacity,
                unused_capacity=tanker.capacity - loaded_volume,
            )
        )

        remaining_cargo_volume -= loaded_volume

        if remaining_cargo_volume == 0:
            cargo_index += 1
            if cargo_index < len(payload.cargo):
                remaining_cargo_volume = payload.cargo[cargo_index].cubic_volume

    if cargo_index < len(payload.cargo):
        if remaining_cargo_volume > 0:
            unallocated_cargo.append(
                UnallocatedCargoItem(
                    cargo_id=payload.cargo[cargo_index].id,
                    remaining_volume=remaining_cargo_volume,
                )
            )

        for cargo in payload.cargo[cargo_index + 1 :]:
            unallocated_cargo.append(
                UnallocatedCargoItem(
                    cargo_id=cargo.id,
                    remaining_volume=cargo.cubic_volume,
                )
            )

    total_cargo_volume = sum(cargo.cubic_volume for cargo in payload.cargo)
    total_tanker_capacity = sum(tanker.capacity for tanker in payload.tankers)
    total_loaded_volume = sum(allocation.loaded_volume for allocation in allocations)
    total_unallocated_volume = sum(cargo.remaining_volume for cargo in unallocated_cargo)

    return AllocationOptimizationResponse(
        message="Allocation optimization completed",
        total_cargo_volume=total_cargo_volume,
        total_tanker_capacity=total_tanker_capacity,
        total_loaded_volume=total_loaded_volume,
        total_unallocated_volume=total_unallocated_volume,
        allocations=allocations,
        unallocated_cargo=unallocated_cargo,
    )
