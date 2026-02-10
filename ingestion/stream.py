from __future__ import annotations
import asyncio
import random
from typing import Dict, List

from ingestion.generator import sensor_stream_simulator


async def poll_sensor(sensor_id: str, delay_seconds: float = 0.1) -> Dict[str, float]:
    """
    Asynchronously poll a single sensor after a simulated network delay.

    Args:
        sensor_id: Unique sensor identifier.
        delay_seconds: Simulated network latency in seconds.

    Returns:
        Dict[str, float]: One sensor reading.
    """
    if delay_seconds < 0:
        raise ValueError("delay_seconds must be non-negative")

    # Simulate network I/O latency (NON-BLOCKING)
    await asyncio.sleep(delay_seconds)

    stream = sensor_stream_simulator(sensor_id)
    reading = next(stream)
    return reading


async def poll_sector(sensor_ids: List[str], delay_seconds: float = 0.1) -> List[Dict[str, float]]:
    """
    Poll multiple sensors concurrently using asyncio.gather().

    Args:
        sensor_ids: List of sensor IDs to poll.
        delay_seconds: Simulated per-sensor network latency.

    Returns:
        List[Dict[str, float]]: List of sensor readings.
    """
    if not sensor_ids:
        raise ValueError("sensor_ids must not be empty")

    tasks = [
        poll_sensor(sensor_id, delay_seconds=delay_seconds)
        for sensor_id in sensor_ids
    ]

    # Run all sensor polls concurrently
    results = await asyncio.gather(*tasks)
    return results
