import { useEffect, useState } from "react";

import {
  type AllocationOptimizationResponse,
  getOptimizationResults,
  runOptimization,
  uploadAllocationInput
} from "./api/cargoAllocation";
import { getHealth } from "./api/health";

type ApiStatus = "checking" | "online" | "offline";
type RequestStatus = "idle" | "loading";
type EditableRow = {
  id: string;
  value: string;
};

const initialCargoRows: EditableRow[] = [
  { id: "C1", value: "120" },
  { id: "C2", value: "80" }
];

const initialTankerRows: EditableRow[] = [
  { id: "T1", value: "100" },
  { id: "T2", value: "100" }
];

function toNumber(value: string): number {
  return Number.parseFloat(value);
}

function formatVolume(value: number): string {
  return new Intl.NumberFormat("en", {
    maximumFractionDigits: 2
  }).format(value);
}

function App() {
  const [apiStatus, setApiStatus] = useState<ApiStatus>("checking");
  const [cargoRows, setCargoRows] = useState<EditableRow[]>(initialCargoRows);
  const [tankerRows, setTankerRows] = useState<EditableRow[]>(initialTankerRows);
  const [results, setResults] = useState<AllocationOptimizationResponse | null>(null);
  const [inputSaved, setInputSaved] = useState(false);
  const [requestStatus, setRequestStatus] = useState<RequestStatus>("idle");
  const [notice, setNotice] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;

    getHealth()
      .then(() => {
        if (isMounted) {
          setApiStatus("online");
        }
      })
      .catch(() => {
        if (isMounted) {
          setApiStatus("offline");
        }
      });

    return () => {
      isMounted = false;
    };
  }, []);

  const cargoTotal = cargoRows.reduce((total, row) => total + (toNumber(row.value) || 0), 0);
  const tankerTotal = tankerRows.reduce((total, row) => total + (toNumber(row.value) || 0), 0);
  const unusedTankerCapacity =
    results?.allocations.reduce((total, item) => total + item.unused_capacity, 0) ?? 0;

  function updateCargoRow(index: number, field: keyof EditableRow, value: string) {
    setInputSaved(false);
    setResults(null);
    setCargoRows((rows) =>
      rows.map((row, rowIndex) => (rowIndex === index ? { ...row, [field]: value } : row))
    );
  }

  function updateTankerRow(index: number, field: keyof EditableRow, value: string) {
    setInputSaved(false);
    setResults(null);
    setTankerRows((rows) =>
      rows.map((row, rowIndex) => (rowIndex === index ? { ...row, [field]: value } : row))
    );
  }

  function addCargoRow() {
    setInputSaved(false);
    setResults(null);
    setCargoRows((rows) => [...rows, { id: `C${rows.length + 1}`, value: "" }]);
  }

  function addTankerRow() {
    setInputSaved(false);
    setResults(null);
    setTankerRows((rows) => [...rows, { id: `T${rows.length + 1}`, value: "" }]);
  }

  function removeCargoRow(index: number) {
    setInputSaved(false);
    setResults(null);
    setCargoRows((rows) => rows.filter((_, rowIndex) => rowIndex !== index));
  }

  function removeTankerRow(index: number) {
    setInputSaved(false);
    setResults(null);
    setTankerRows((rows) => rows.filter((_, rowIndex) => rowIndex !== index));
  }

  function buildPayload() {
    const cargo = cargoRows.map((row) => ({
      id: row.id.trim(),
      cubic_volume: toNumber(row.value)
    }));
    const tankers = tankerRows.map((row) => ({
      id: row.id.trim(),
      capacity: toNumber(row.value)
    }));

    const hasInvalidCargo = cargo.some(
      (item) => !item.id || !Number.isFinite(item.cubic_volume) || item.cubic_volume <= 0
    );
    const hasInvalidTankers = tankers.some(
      (item) => !item.id || !Number.isFinite(item.capacity) || item.capacity <= 0
    );

    if (!cargo.length || !tankers.length || hasInvalidCargo || hasInvalidTankers) {
      throw new Error("Enter valid IDs and positive volumes before submitting.");
    }

    return { cargo, tankers };
  }

  async function handleSaveInput() {
    setRequestStatus("loading");
    setError(null);
    setNotice(null);

    try {
      const payload = buildPayload();
      await uploadAllocationInput(payload);
      setInputSaved(true);
      setResults(null);
      setNotice("Input saved");
    } catch (caughtError) {
      setError(caughtError instanceof Error ? caughtError.message : "Unable to save input");
    } finally {
      setRequestStatus("idle");
    }
  }

  async function handleOptimize() {
    setRequestStatus("loading");
    setError(null);
    setNotice(null);

    try {
      if (!inputSaved) {
        const payload = buildPayload();
        await uploadAllocationInput(payload);
        setInputSaved(true);
      }

      const optimizationResult = await runOptimization();
      setResults(optimizationResult);
      setNotice("Optimization complete");
    } catch (caughtError) {
      setError(caughtError instanceof Error ? caughtError.message : "Unable to optimize allocation");
    } finally {
      setRequestStatus("idle");
    }
  }

  async function handleFetchResults() {
    setRequestStatus("loading");
    setError(null);
    setNotice(null);

    try {
      const latestResults = await getOptimizationResults();
      setResults(latestResults);
      setNotice("Latest results loaded");
    } catch (caughtError) {
      setError(caughtError instanceof Error ? caughtError.message : "Unable to load results");
    } finally {
      setRequestStatus("idle");
    }
  }

  return (
    <main className="app-shell">
      <section className="workspace">
        <div className="toolbar">
          <div>
            <p className="eyebrow">Cargo Allocation System</p>
            <h1>Allocation Dashboard</h1>
          </div>
          <div className={`status-pill status-pill--${apiStatus}`}>
            <span aria-hidden="true" />
            API {apiStatus}
          </div>
        </div>

        <div className="summary-grid">
          <article className="metric-card">
            <p>Cargo Volume</p>
            <strong>{formatVolume(results?.total_cargo_volume ?? cargoTotal)}</strong>
          </article>
          <article className="metric-card">
            <p>Tanker Capacity</p>
            <strong>{formatVolume(results?.total_tanker_capacity ?? tankerTotal)}</strong>
          </article>
          <article className="metric-card">
            <p>Allocated Volume</p>
            <strong>{formatVolume(results?.total_loaded_volume ?? 0)}</strong>
          </article>
        </div>

        <div className="action-bar">
          <button type="button" onClick={handleSaveInput} disabled={requestStatus === "loading"}>
            Save input
          </button>
          <button
            type="button"
            className="button-primary"
            onClick={handleOptimize}
            disabled={requestStatus === "loading"}
          >
            Run optimization
          </button>
          <button type="button" onClick={handleFetchResults} disabled={requestStatus === "loading"}>
            Load results
          </button>
        </div>

        {notice ? <div className="alert alert-success">{notice}</div> : null}
        {error ? <div className="alert alert-error">{error}</div> : null}

        <div className="input-grid">
          <section className="panel">
            <div className="panel-header">
              <h2>Cargo</h2>
              <button type="button" className="button-compact" onClick={addCargoRow}>
                Add
              </button>
            </div>
            <div className="data-table">
              <div className="table-row table-row-head">
                <span>ID</span>
                <span>Cubic volume</span>
                <span />
              </div>
              {cargoRows.map((row, index) => (
                <div className="table-row" key={`cargo-${index}`}>
                  <input
                    aria-label={`Cargo ${index + 1} ID`}
                    value={row.id}
                    onChange={(event) => updateCargoRow(index, "id", event.target.value)}
                  />
                  <input
                    aria-label={`Cargo ${index + 1} cubic volume`}
                    type="number"
                    min="0"
                    step="0.01"
                    value={row.value}
                    onChange={(event) => updateCargoRow(index, "value", event.target.value)}
                  />
                  <button
                    type="button"
                    className="button-icon"
                    aria-label={`Remove cargo ${index + 1}`}
                    onClick={() => removeCargoRow(index)}
                    disabled={cargoRows.length === 1}
                  >
                    x
                  </button>
                </div>
              ))}
            </div>
          </section>

          <section className="panel">
            <div className="panel-header">
              <h2>Tankers</h2>
              <button type="button" className="button-compact" onClick={addTankerRow}>
                Add
              </button>
            </div>
            <div className="data-table">
              <div className="table-row table-row-head">
                <span>ID</span>
                <span>Capacity</span>
                <span />
              </div>
              {tankerRows.map((row, index) => (
                <div className="table-row" key={`tanker-${index}`}>
                  <input
                    aria-label={`Tanker ${index + 1} ID`}
                    value={row.id}
                    onChange={(event) => updateTankerRow(index, "id", event.target.value)}
                  />
                  <input
                    aria-label={`Tanker ${index + 1} capacity`}
                    type="number"
                    min="0"
                    step="0.01"
                    value={row.value}
                    onChange={(event) => updateTankerRow(index, "value", event.target.value)}
                  />
                  <button
                    type="button"
                    className="button-icon"
                    aria-label={`Remove tanker ${index + 1}`}
                    onClick={() => removeTankerRow(index)}
                    disabled={tankerRows.length === 1}
                  >
                    x
                  </button>
                </div>
              ))}
            </div>
          </section>
        </div>

        <section className="panel results-panel">
          <div className="panel-header">
            <h2>Optimized Allocation</h2>
            {results ? (
              <div className="result-summary">
                <span>Unallocated cargo {formatVolume(results.total_unallocated_volume)}</span>
                <span>Unused capacity {formatVolume(unusedTankerCapacity)}</span>
              </div>
            ) : null}
          </div>

          {results ? (
            <>
              <div className="results-table">
                <div className="results-row results-row-head">
                  <span>Tanker</span>
                  <span>Cargo</span>
                  <span>Loaded</span>
                  <span>Capacity</span>
                  <span>Unused</span>
                </div>
                {results.allocations.map((allocation) => (
                  <div className="results-row" key={`${allocation.tanker_id}-${allocation.cargo_id}`}>
                    <span>{allocation.tanker_id}</span>
                    <span>{allocation.cargo_id}</span>
                    <span>{formatVolume(allocation.loaded_volume)}</span>
                    <span>{formatVolume(allocation.tanker_capacity)}</span>
                    <span>{formatVolume(allocation.unused_capacity)}</span>
                  </div>
                ))}
              </div>

              {results.unallocated_cargo.length ? (
                <div className="unallocated-list">
                  {results.unallocated_cargo.map((cargo) => (
                    <span key={cargo.cargo_id}>
                      {cargo.cargo_id}: {formatVolume(cargo.remaining_volume)}
                    </span>
                  ))}
                </div>
              ) : null}
            </>
          ) : (
            <div className="empty-state">No optimization result loaded</div>
          )}
        </section>
      </section>
    </main>
  );
}

export default App;
