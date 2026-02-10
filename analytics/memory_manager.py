from __future__ import annotations

import gc
import weakref
from typing import Any


class SensorCache:
    """
    Cache for active sensor objects using WeakValueDictionary.
    Objects disappear automatically when no strong references remain.
    """

    def __init__(self) -> None:
        self._cache: weakref.WeakValueDictionary[str, Any] = weakref.WeakValueDictionary()

    def add(self, sensor_id: str, sensor_obj: Any) -> None:
        if not sensor_id:
            raise ValueError("sensor_id must be a non-empty string")
        self._cache[sensor_id] = sensor_obj

    def get(self, sensor_id: str) -> Any | None:
        return self._cache.get(sensor_id)

    def size(self) -> int:
        return len(self._cache)

    def clear(self) -> None:
        self._cache.clear()


def force_cleanup() -> int:
    """
    Force garbage collection after heavy analytics processing.

    Returns:
        int: Number of unreachable objects collected.
    """
    return gc.collect()
