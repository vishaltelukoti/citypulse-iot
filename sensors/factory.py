from __future__ import annotations
from core.meta import SensorMeta
from core.interfaces import AbstractSensor


class DeviceFactory:
    """
    Factory responsible for creating sensor instances using the registry.
    """

    @staticmethod
    def create_device(sensor_type: str, device_id: str) -> AbstractSensor:
        if not sensor_type:
            raise ValueError("sensor_type must be provided")

        registry = SensorMeta.get_registry()

        if sensor_type not in registry:
            raise ValueError(f"Unknown sensor type: {sensor_type}")

        sensor_class = registry[sensor_type]
        return sensor_class(device_id)
