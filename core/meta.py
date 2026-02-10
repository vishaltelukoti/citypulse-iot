from __future__ import annotations
from abc import ABCMeta
from typing import Dict, Type


class SensorMeta(ABCMeta):
    """
    Metaclass that auto-registers all concrete sensor classes.
    """
    _registry: Dict[str, Type] = {}

    def __new__(mcls, name, bases, namespace, **kwargs):
        cls = super().__new__(mcls, name, bases, namespace, **kwargs)

        # Avoid registering the abstract base class itself
        if name != "AbstractSensor":
            SensorMeta._registry[name] = cls

        return cls

    @classmethod
    def get_registry(mcls) -> Dict[str, Type]:
        return dict(mcls._registry)
