from __future__ import annotations

import asyncio
import os
import sqlite3
from typing import List

from analytics import SensorCache, force_cleanup, calculate_heatmap_index
from analytics.strategies import WiFiStrategy, LoRaWanStrategy
from config import GridConfig
from core.events import EmergencyResponseSystem
from ingestion import poll_sector
from security import (
    generate_sha256,
    generate_fernet_key,
    encrypt_data,
    decrypt_data,
    safe_log_path,
    get_sensor_by_id,
)
from sensors import DeviceFactory, TrafficSensor, FireSensor


LOG_BASE_DIR = os.path.join(os.getcwd(), "var", "logs")
DEFAULT_POLL_DELAY = 0.1
SAMPLE_SENSORS = ["TrafficSensor", "TrafficSensor", "TrafficSensor"]


class ConsoleSubscriber:
    """Simple subscriber that prints emergency alerts to console."""

    def notify(self, message: str) -> None:
        print(message)


def setup_demo_database() -> sqlite3.Connection:
    """
    Create an in-memory SQLite database for demonstrating
    safe parameterized queries.
    """
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE sensors (id TEXT PRIMARY KEY, name TEXT)")
    cur.execute("INSERT INTO sensors (id, name) VALUES (?, ?)", ("SENSOR-1", "Traffic"))
    conn.commit()
    return conn


async def run_ingestion_demo() -> None:
    """
    Demonstrate async ingestion using asyncio.gather().
    """
    sensor_ids: List[str] = [f"SENSOR-{i}" for i in range(1, 101)]
    results = await poll_sector(sensor_ids, delay_seconds=DEFAULT_POLL_DELAY)
    print(f"[Ingestion] Collected {len(results)} sensor readings.")


def run_security_demo() -> None:
    """
    Demonstrate hashing, encryption, safe SQL, and safe file paths.
    """
    # Hashing
    payload = b'{"sensor":"SENSOR-1","value":42}'
    digest = generate_sha256(payload)
    print(f"[Security] SHA-256 digest: {digest}")

    # Encryption / Decryption (e.g., GPS coordinates)
    key = generate_fernet_key()
    secret_data = b"12.9716,77.5946"  # Example GPS coordinates
    token = encrypt_data(secret_data, key)
    recovered = decrypt_data(token, key)
    print(f"[Security] Encrypted token length: {len(token)} bytes")
    print(f"[Security] Decrypted data: {recovered.decode()}")

    # Safe file path
    os.makedirs(LOG_BASE_DIR, exist_ok=True)
    log_path = safe_log_path(LOG_BASE_DIR, "TrafficSensor")
    print(f"[Security] Safe log path: {log_path}")

    # Safe SQL
    conn = setup_demo_database()
    row = get_sensor_by_id(conn, "105 OR 1=1")  # Injection attempt should fail safely
    print(f"[Security] Query result for injection attempt: {row}")
    conn.close()


def run_architecture_demo() -> None:
    """
    Demonstrate Part-1 architecture: Factory, Singleton, Observer, Strategy.
    """
    # Singleton config
    config = GridConfig()
    print(f"[Config] Fire threshold: {config.get('fire_threshold_celsius')} °C")

    # Observer system
    emergency_system = EmergencyResponseSystem()
    emergency_system.subscribe(ConsoleSubscriber())

    # Create sensors via factory (TrafficSensor auto-registered)
    traffic_sensor = DeviceFactory.create_device("TrafficSensor", "TRAFFIC-001")

    # FireSensor needs emergency system, so instantiate directly (still registered)
    fire_sensor = FireSensor("FIRE-001", emergency_system)

    print(f"[Sensors] Traffic reading: {traffic_sensor.read_stream()}")
    print(f"[Sensors] Fire reading: {fire_sensor.read_stream()}")

    # Strategy pattern
    data = "X" * 100
    wifi = WiFiStrategy()
    lora = LoRaWanStrategy()

    wifi_data = wifi.transmit(data)
    lora_data = lora.transmit(data)

    print(f"[Strategy] WiFi data size: {len(wifi_data)}")
    print(f"[Strategy] LoRaWAN data size: {len(lora_data)}")


def run_performance_demo() -> None:
    """
    Demonstrate Part-3: NumPy vectorized calculation and memory cleanup.
    """
    import numpy as np

    temperature = np.random.uniform(10, 50, size=1_000_000)
    humidity = np.random.uniform(10, 90, size=1_000_000)
    co2 = np.random.uniform(300, 2000, size=1_000_000)

    index = calculate_heatmap_index(temperature, humidity, co2)
    print(f"[Performance] Heatmap index computed for {len(index)} rows.")

    # WeakRef cache demo
    cache = SensorCache()

    class HeavyObject:
        def __init__(self) -> None:
            self.data = [0] * 1_000_000

    heavy = HeavyObject()
    cache.add("heavy", heavy)
    print(f"[Memory] Cache size before delete: {cache.size()}")

    del heavy
    collected = force_cleanup()
    print(f"[Memory] GC collected {collected} objects.")
    print(f"[Memory] Cache size after GC: {cache.size()}")


async def main() -> None:
    """
    Main async entry point for CityPulse IoT demo.
    """
    print("=== CityPulse IoT Demo Starting ===")

    run_architecture_demo()
    run_security_demo()
    run_performance_demo()
    await run_ingestion_demo()

    print("=== CityPulse IoT Demo Finished ===")


if __name__ == "__main__":
    asyncio.run(main())
