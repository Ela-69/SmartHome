from typing import Optional

from devices import IDevice, ILockable
from home_configuration import HomeConfiguration


class SmartHomeFacade:
    def __init__(self, light: IDevice, fan: IDevice, door: ILockable,
                 config: Optional[HomeConfiguration] = None) -> None:
        if not isinstance(door, ILockable):
            raise TypeError("door must implement ILockable")
        self._light = light
        self._fan = fan
        self._door = door
        self._config = config or HomeConfiguration.instance()

    def go_to_work(self) -> None:
        self._light.turn_off()
        self._fan.turn_off()
        self._door.lock()

    def go_to_sleep(self) -> None:
        self._fan.turn_off()
        self._door.lock()
        self._light.turn_on()
        print(f"Night light level: {self._config.night_light_level}%")
