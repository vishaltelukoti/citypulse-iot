"""
Sensors package for CityPulse IoT.

This package contains:
- factory.py: DeviceFactory for creating sensor instances from the registry.
- implementations.py: Concrete sensor implementations (e.g., TrafficSensor, FireSensor).
"""

from sensors.factory import DeviceFactory
from sensors.implementations import TrafficSensor, FireSensor

__all__ = [
    "DeviceFactory",
    "TrafficSensor",
    "FireSensor",
]
