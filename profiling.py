from __future__ import annotations

import cProfile
import pstats
import io
import tracemalloc
import asyncio

from main import main


def run_cpu_profile() -> None:
    profiler = cProfile.Profile()
    profiler.enable()

    asyncio.run(main())

    profiler.disable()

    s = io.StringIO()
    stats = pstats.Stats(profiler, stream=s).sort_stats("cumulative")
    stats.print_stats(30)  # top 30 functions

    print("=== CPU PROFILE (Top 30) ===")
    print(s.getvalue())


def run_memory_profile() -> None:
    tracemalloc.start()

    asyncio.run(main())

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("=== MEMORY PROFILE ===")
    print(f"Current memory: {current / 1024 / 1024:.2f} MB")
    print(f"Peak memory: {peak / 1024 / 1024:.2f} MB")


if __name__ == "__main__":
    print("Running CPU profiling...")
    run_cpu_profile()

    print("\nRunning Memory profiling...")
    run_memory_profile()
