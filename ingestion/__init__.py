"""
Ingestion package for CityPulse IoT.

This package handles real-time data ingestion from sensors, including:
- generator.py: Infinite data stream simulators using generators (yield).
- stream.py: Async polling logic using asyncio and asyncio.gather().
"""

from ingestion.generator import sensor_stream_simulator
from ingestion.stream import poll_sensor, poll_sector

__all__ = [
    "sensor_stream_simulator",
    "poll_sensor",
    "poll_sector",
]
