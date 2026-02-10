from __future__ import annotations

import asyncio
import sqlite3
import time
import unittest
import gc

import numpy as np

from core.meta import SensorMeta
from analytics.strategies import WiFiStrategy, LoRaWanStrategy
from ingestion.stream import poll_sector
from analytics.memory_manager import SensorCache, force_cleanup
from security.sanitizer import get_sensor_by_id
from analytics.processor import calculate_heatmap_index


class TestCityPulse(unittest.TestCase):
    """
    Mandatory test suite for CityPulse IoT capstone project.
    Covers all 6 required test cases from the specification.
    """

    # Test Case 1: Metaclass Registry
    def test_metaclass_registry(self) -> None:
        class WaterLevel(metaclass=SensorMeta):
            def __init__(self, device_id: str) -> None:
                self.device_id = device_id

            def read_stream(self):
                return {"level": 42}

            def health_check(self):
                return True

        registry = SensorMeta.get_registry()
        self.assertIn("WaterLevel", registry)

    # Test Case 2: Strategy Swap
    def test_strategy_swap(self) -> None:
        data = "X" * 1000  # Large payload

        wifi = WiFiStrategy()
        lora = LoRaWanStrategy()

        wifi_data = wifi.transmit(data)
        lora_data = lora.transmit(data)

        self.assertEqual(len(wifi_data), len(data))
        self.assertLess(len(lora_data), len(wifi_data))


    # Test Case 3: Async Performance
    def test_async_performance(self) -> None:
        sensor_ids = [f"SENSOR-{i}" for i in range(100)]

        start = time.perf_counter()
        asyncio.run(poll_sector(sensor_ids, delay_seconds=0.1))
        elapsed = time.perf_counter() - start

        # Should be close to ~0.1–0.2 seconds, not ~10 seconds
        self.assertLess(elapsed, 1.0, f"Async polling too slow: {elapsed} seconds")

    # Test Case 4: Memory Leak Check (WeakValueDictionary)
    def test_memory_leak_check(self) -> None:
        cache = SensorCache()

        class HeavySensor:
            def __init__(self) -> None:
                self.data = [0] * 10_000_00  # Large object (~8MB+)

        sensor = HeavySensor()
        cache.add("heavy", sensor)

        self.assertEqual(cache.size(), 1)

        # Remove strong reference
        del sensor
        collected = force_cleanup()

        # Force Python GC as well (extra safety)
        gc.collect()

        self.assertEqual(cache.size(), 0)

    
    # Test Case 5: Secure SQL (No Injection)

    def test_secure_sql(self) -> None:
        # Setup in-memory DB
        conn = sqlite3.connect(":memory:")
        cur = conn.cursor()
        cur.execute("CREATE TABLE sensors (id TEXT PRIMARY KEY, name TEXT)")
        cur.execute("INSERT INTO sensors (id, name) VALUES (?, ?)", ("105", "TestSensor"))
        conn.commit()

        # Injection attempt
        user_input = "105 OR 1=1"
        result = get_sensor_by_id(conn, user_input)

        # Should return None, not all rows
        self.assertIsNone(result)

        conn.close()


    # Test Case 6: NumPy Speedup
    def test_numpy_speedup(self) -> None:
        n = 1_000_000

        temperature = np.random.uniform(10, 50, size=n)
        humidity = np.random.uniform(10, 90, size=n)
        co2 = np.random.uniform(300, 2000, size=n)

        # Python loop version
        start = time.perf_counter()
        result_loop = []
        for t, h, c in zip(temperature, humidity, co2):
            result_loop.append(0.5 * t + 0.3 * h + 0.2 * np.log(c))
        loop_time = time.perf_counter() - start

        # NumPy vectorized version
        start = time.perf_counter()
        _ = calculate_heatmap_index(temperature, humidity, co2)
        numpy_time = time.perf_counter() - start

        # NumPy should be MUCH faster
        self.assertGreater(loop_time / numpy_time, 30, "NumPy is not significantly faster than loop")


if __name__ == "__main__":
    unittest.main()
