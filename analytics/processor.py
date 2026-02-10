from __future__ import annotations

import time
from typing import Tuple

import numpy as np
import pandas as pd


def resample_per_minute(df: pd.DataFrame) -> pd.DataFrame:
    """
    Resample per-second sensor data to per-minute averages.

    The DataFrame must have:
    - A DateTimeIndex
    - Columns: temperature, humidity, co2

    Returns:
        pd.DataFrame: Resampled per-minute averages.
    """
    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError("DataFrame index must be a pandas.DatetimeIndex")

    required_columns = {"temperature", "humidity", "co2"}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"DataFrame must contain columns: {required_columns}")

    return df.resample("1min").mean()


def calculate_heatmap_index(
    temperature: np.ndarray,
    humidity: np.ndarray,
    co2: np.ndarray,
) -> np.ndarray:
    """
    Vectorized calculation of Heatmap Index.

    Formula (example composite index):
        index = 0.5 * temperature + 0.3 * humidity + 0.2 * log(co2)

    Constraints:
        - NO Python loops
        - Must be fully vectorized NumPy operations

    Returns:
        np.ndarray: Heatmap index values.
    """
    if not (len(temperature) == len(humidity) == len(co2)):
        raise ValueError("All input arrays must have the same length")

    temperature = np.asarray(temperature, dtype=np.float64)
    humidity = np.asarray(humidity, dtype=np.float64)
    co2 = np.asarray(co2, dtype=np.float64)

    # Vectorized computation (NO loops)
    index = 0.5 * temperature + 0.3 * humidity + 0.2 * np.log(co2)

    return index


def benchmark_numpy_vs_loop(n: int = 10_000_00) -> Tuple[float, float]:
    """
    Benchmark NumPy vectorized calculation vs Python loop.

    Returns:
        Tuple[float, float]: (loop_time, numpy_time)
    """
    temperature = np.random.uniform(10, 50, size=n)
    humidity = np.random.uniform(10, 90, size=n)
    co2 = np.random.uniform(300, 2000, size=n)

    # Python loop (slow)
    start = time.perf_counter()
    result_loop = []
    for t, h, c in zip(temperature, humidity, co2):
        result_loop.append(0.5 * t + 0.3 * h + 0.2 * np.log(c))
    loop_time = time.perf_counter() - start

    # NumPy vectorized (fast)
    start = time.perf_counter()
    _ = calculate_heatmap_index(temperature, humidity, co2)
    numpy_time = time.perf_counter() - start

    return loop_time, numpy_time
