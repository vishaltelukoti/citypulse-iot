from __future__ import annotations
from typing import List, Protocol


class Subscriber(Protocol):
    def notify(self, message: str) -> None:
        ...


class EmergencyResponseSystem:
    """
    Observer system that notifies all subscribers about critical events.
    """

    def __init__(self) -> None:
        self._subscribers: List[Subscriber] = []

    def subscribe(self, subscriber: Subscriber) -> None:
        if subscriber not in self._subscribers:
            self._subscribers.append(subscriber)

    def unsubscribe(self, subscriber: Subscriber) -> None:
        if subscriber in self._subscribers:
            self._subscribers.remove(subscriber)

    def notify_all(self, message: str) -> None:
        for subscriber in self._subscribers:
            subscriber.notify(message)
