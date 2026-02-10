from __future__ import annotations

import os
import re
import sqlite3
from typing import Optional


SAFE_FILENAME_PATTERN = re.compile(r"^[a-zA-Z0-9_\-\.]+$")


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent directory traversal and invalid characters.

    Only allows: letters, numbers, underscore, dash, dot.

    Args:
        filename: User-provided filename.

    Returns:
        str: Safe filename.

    Raises:
        ValueError: If filename is unsafe.
    """
    if not filename:
        raise ValueError("Filename must not be empty")

    if not SAFE_FILENAME_PATTERN.match(filename):
        raise ValueError("Unsafe filename detected")

    return filename


def safe_log_path(base_dir: str, sensor_name: str) -> str:
    """
    Build a safe log file path for a sensor.

    Args:
        base_dir: Base logs directory.
        sensor_name: Sensor name (user input).

    Returns:
        str: Safe absolute path.
    """
    safe_name = sanitize_filename(sensor_name)
    path = os.path.join(base_dir, f"{safe_name}.txt")
    return os.path.abspath(path)


def get_sensor_by_id(conn: sqlite3.Connection, user_input: str) -> Optional[tuple]:
    """
    Safely query sensor by ID using parameterized query
    to prevent SQL injection.

    Args:
        conn: sqlite3 connection
        user_input: Raw user input for sensor ID

    Returns:
        Optional[tuple]: Row if found, else None
    """
    query = "SELECT * FROM sensors WHERE id = ?"
    cursor = conn.cursor()
    cursor.execute(query, (user_input,))
    return cursor.fetchone()
