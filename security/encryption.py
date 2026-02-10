from __future__ import annotations

import hashlib
from typing import Tuple

from cryptography.fernet import Fernet


def generate_sha256(data: bytes) -> str:
    """
    Generate SHA-256 hash of given data for integrity verification.

    Args:
        data: Raw bytes to hash.

    Returns:
        str: Hexadecimal SHA-256 digest.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("Data must be bytes")

    sha = hashlib.sha256()
    sha.update(data)
    return sha.hexdigest()


def generate_fernet_key() -> bytes:
    """
    Generate a new Fernet key.

    Returns:
        bytes: Fernet key.
    """
    return Fernet.generate_key()


def encrypt_data(data: bytes, key: bytes) -> bytes:
    """
    Encrypt sensitive data using Fernet symmetric encryption.

    Args:
        data: Plaintext bytes.
        key: Fernet key.

    Returns:
        bytes: Encrypted token.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("Data must be bytes")

    fernet = Fernet(key)
    return fernet.encrypt(data)


def decrypt_data(token: bytes, key: bytes) -> bytes:
    """
    Decrypt Fernet encrypted data.

    Args:
        token: Encrypted token.
        key: Fernet key.

    Returns:
        bytes: Decrypted plaintext.
    """
    fernet = Fernet(key)
    return fernet.decrypt(token)
