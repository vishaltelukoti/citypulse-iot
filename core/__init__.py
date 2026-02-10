"""
Ingestion package for CityPulse IoT.

This package contains:
- generator.py: Infinite data stream simulators using generators.
- stream.py: Async polling logic using asyncio for concurrent sensor ingestion.
"""

from ingestion.generator import sensor_stream_simulator
from ingestion.stream import poll_sensor, poll_sector

__all__ = [
    "sensor_stream_simulator",
    "poll_sensor",
    "poll_sector",
]

