from __future__ import annotations
from typing import Any, Dict


class GridConfig:
    """
    Singleton configuration manager for the CityPulse grid.
    """

    _instance: "GridConfig | None" = None

    DEFAULTS: Dict[str, Any] = {
        "api_endpoint": "https://api.citypulse.local",
        "fire_threshold_celsius": 80.0,
    }

    def __new__(cls) -> "GridConfig":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._config = dict(cls.DEFAULTS)
        return cls._instance

    def get(self, key: str) -> Any:
        return self._config.get(key)

    def set(self, key: str, value: Any) -> None:
        self._config[key] = value
