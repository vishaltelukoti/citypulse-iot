from __future__ import annotations
import random
from typing import Dict, Any

from core.interfaces import AbstractSensor
from core.events import EmergencyResponseSystem
from config import GridConfig


ABSOLUTE_ZERO_CELSIUS: float = -273.15


class TrafficSensor(AbstractSensor):
    """
    Simulates traffic density sensor.
    """

    def read_stream(self) -> Dict[str, Any]:
        cars_per_min = random.randint(0, 200)
        return {"cars_per_min": cars_per_min}

    def health_check(self) -> bool:
        return True


class FireSensor(AbstractSensor):
    """
    Simulates a fire/temperature sensor and triggers alerts if threshold exceeded.
    """

    def __init__(self, device_id: str, emergency_system: EmergencyResponseSystem):
        super().__init__(device_id)
        self._emergency_system = emergency_system
        self._config = GridConfig()

    def read_stream(self) -> Dict[str, Any]:
        temperature = random.uniform(20.0, 120.0)

        if temperature < ABSOLUTE_ZERO_CELSIUS:
            raise ValueError("Invalid temperature: below absolute zero")

        threshold = self._config.get("fire_threshold_celsius")

        if temperature > threshold:
            self._emergency_system.notify_all(
                f" FIRE ALERT from {self.device_id}: {temperature:.2f} °C"
            )

        return {"temperature_celsius": temperature}

    def health_check(self) -> bool:
        return True
