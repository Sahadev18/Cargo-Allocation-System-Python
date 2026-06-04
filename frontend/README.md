# Cargo Allocation Frontend

React frontend for the Cargo Allocation System.

## Setup

Install dependencies:

```powershell
npm install
```

Copy the example environment file:

```powershell
Copy-Item .env.example .env
```

Run the development server:

```powershell
npm run dev
```

The app will be available at `http://localhost:5173`.

## Docker

Build the frontend image from the frontend folder:

```powershell
docker build -t cargo-allocation-frontend .
```

Run the container:

```powershell
docker run --rm -p 3000:80 cargo-allocation-frontend
```

The app will be available at `http://localhost:3000`.

## Scripts

- `npm run dev` starts the local Vite server.
- `npm run build` type-checks and builds the app.
- `npm run lint` runs ESLint.
- `npm run preview` serves the production build locally.
