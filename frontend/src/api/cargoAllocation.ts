export type CargoInput = {
  id: string;
  cubic_volume: number;
};

export type TankerInput = {
  id: string;
  capacity: number;
};

export type AllocationInputPayload = {
  cargo: CargoInput[];
  tankers: TankerInput[];
};

export type AllocationInputResponse = {
  message: string;
  cargo_count: number;
  tanker_count: number;
};

export type AllocationItem = {
  cargo_id: string;
  tanker_id: string;
  loaded_volume: number;
  tanker_capacity: number;
  unused_capacity: number;
};

export type UnallocatedCargoItem = {
  cargo_id: string;
  remaining_volume: number;
};

export type AllocationOptimizationResponse = {
  message: string;
  total_cargo_volume: number;
  total_tanker_capacity: number;
  total_loaded_volume: number;
  total_unallocated_volume: number;
  allocations: AllocationItem[];
  unallocated_cargo: UnallocatedCargoItem[];
};

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "";

async function parseError(response: Response): Promise<string> {
  try {
    const payload = (await response.json()) as { detail?: string };
    return payload.detail ?? "Request failed";
  } catch {
    return "Request failed";
  }
}

export async function uploadAllocationInput(
  payload: AllocationInputPayload
): Promise<AllocationInputResponse> {
  const response = await fetch(`${apiBaseUrl}/api/v1/cargo-allocation/input`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    throw new Error(await parseError(response));
  }

  return response.json() as Promise<AllocationInputResponse>;
}

export async function runOptimization(): Promise<AllocationOptimizationResponse> {
  const response = await fetch(`${apiBaseUrl}/api/v1/cargo-allocation/optimize`, {
    method: "POST"
  });

  if (!response.ok) {
    throw new Error(await parseError(response));
  }

  return response.json() as Promise<AllocationOptimizationResponse>;
}

export async function getOptimizationResults(): Promise<AllocationOptimizationResponse> {
  const response = await fetch(`${apiBaseUrl}/api/v1/cargo-allocation/results`);

  if (!response.ok) {
    throw new Error(await parseError(response));
  }

  return response.json() as Promise<AllocationOptimizationResponse>;
}
