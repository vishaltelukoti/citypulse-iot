from __future__ import annotations
import random
from typing import Dict, Generator


def sensor_stream_simulator(sensor_id: str) -> Generator[Dict[str, float], None, None]:
    """
    Infinite generator that simulates a live hardware sensor data stream.

    Yields:
        Dict[str, float]: A single sensor reading.
    """
    if not sensor_id:
        raise ValueError("sensor_id must be a non-empty string")

    while True:
        yield {
            "sensor_id": sensor_id,
            "temperature_celsius": random.uniform(15.0, 100.0),
            "humidity_percent": random.uniform(10.0, 90.0),
            "co2_ppm": random.uniform(300.0, 2000.0),
        }
