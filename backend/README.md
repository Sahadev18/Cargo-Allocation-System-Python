# Cargo Allocation Backend

FastAPI backend for the Cargo Allocation System.

## Setup

Create a private virtual environment inside the backend folder:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements-dev.txt
```

Copy the example environment file:

```powershell
Copy-Item .env.example .env
```

Run the API:

```powershell
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Docker

Build the backend image from the backend folder:

```powershell
docker build -t cargo-allocation-backend .
```

Run the container:

```powershell
docker run --rm -p 8000:8000 cargo-allocation-backend
```

## Architecture

The backend is organized by feature:

```text
app/
  api/
    router.py
  core/
    config.py
  features/
    base/
      routes.py
    cargo_allocation/
      routes.py
      schemas.py
      store.py
    health/
      routes.py
      schemas.py
```

Future upload and optimization APIs should be added under `app/features/`.

## Useful Endpoints

- `GET /api/v1`
- `POST /api/v1/cargo-allocation/input`
- `POST /api/v1/cargo-allocation/optimize`
- `GET /api/v1/cargo-allocation/results`
- `GET /health`
- `GET /api/v1/health`
- `GET /docs`
- `GET /redoc`
- `GET /openapi.json`

## Tests

```powershell
pytest
```

You can also run commands without activating the environment:

```powershell
.\.venv\Scripts\python -m pytest
.\.venv\Scripts\python -m uvicorn app.main:app --reload
```
