from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Any

from core.meta import SensorMeta


class AbstractSensor(ABC, metaclass=SensorMeta):
    """
    Abstract base class for all sensors in the CityPulse system.
    """

    def __init__(self, device_id: str) -> None:
        if not device_id:
            raise ValueError("device_id must be a non-empty string")
        self.device_id: str = device_id

    @abstractmethod
    def read_stream(self) -> Dict[str, Any]:
        """
        Read a single data point from the sensor stream.
        """
        raise NotImplementedError

    @abstractmethod
    def health_check(self) -> bool:
        """
        Perform a health check on the sensor.
        """
        raise NotImplementedError
