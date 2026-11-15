from typing import Callable, Dict

from devices import IDevice, SmartDoor, SmartFan, SmartLight


class DeviceFactory:
    _registry: Dict[str, Callable[[str], IDevice]] = {
        "light": SmartLight,
        "fan": SmartFan,
        "door": SmartDoor,
    }

    @classmethod
    def register(cls, device_type: str, creator: Callable[[str], IDevice]) -> None:
        cls._registry[device_type.strip().lower()] = creator

    @classmethod
    def create(cls, device_type: str, name: str) -> IDevice:
        if not isinstance(device_type, str):
            raise ValueError(f"Unsupported device type: {device_type!r}")
        creator = cls._registry.get(device_type.strip().lower())
        if creator is None:
            raise ValueError(f"Unsupported device type: {device_type}")
        return creator(name)
