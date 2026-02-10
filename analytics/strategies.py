from __future__ import annotations
from abc import ABC, abstractmethod


class DataTransmissionStrategy(ABC):
    """
    Strategy interface for data transmission.
    """

    @abstractmethod
    def transmit(self, data: str) -> str:
        raise NotImplementedError


class WiFiStrategy(DataTransmissionStrategy):
    """
    Sends full, uncompressed data.
    """

    def transmit(self, data: str) -> str:
        if not isinstance(data, str):
            raise TypeError("Data must be a string")
        return data


class LoRaWanStrategy(DataTransmissionStrategy):
    """
    Simulates compressed transmission by truncating data.
    """

    COMPRESSION_RATIO: float = 0.25  # 25% of original size

    def transmit(self, data: str) -> str:
        if not isinstance(data, str):
            raise TypeError("Data must be a string")

        if not data:
            return data

        new_length = max(1, int(len(data) * self.COMPRESSION_RATIO))
        return data[:new_length]
