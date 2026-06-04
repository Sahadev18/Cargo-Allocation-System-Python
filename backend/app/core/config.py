import json
import os
from dataclasses import dataclass, field


def _get_cors_origins() -> list[str]:
    raw_origins = os.getenv("BACKEND_CORS_ORIGINS")
    if not raw_origins:
        return ["http://localhost:5173", "http://localhost:3000"]

    try:
        parsed_origins = json.loads(raw_origins)
    except json.JSONDecodeError:
        return [origin.strip() for origin in raw_origins.split(",") if origin.strip()]

    if isinstance(parsed_origins, list):
        return [str(origin) for origin in parsed_origins]

    return []


@dataclass(frozen=True)
class Settings:
    app_name: str = "Cargo Allocation API"
    app_env: str = "development"
    api_v1_prefix: str = "/api/v1"
    backend_cors_origins: list[str] = field(default_factory=_get_cors_origins)


settings = Settings(
    app_name=os.getenv("APP_NAME", "Cargo Allocation API"),
    app_env=os.getenv("APP_ENV", "development"),
    api_v1_prefix=os.getenv("API_V1_PREFIX", "/api/v1"),
)
