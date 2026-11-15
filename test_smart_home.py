import io
import unittest
from contextlib import redirect_stdout

from device_factory import DeviceFactory
from devices import IDevice, ILockable, SmartDoor, SmartFan, SmartLight
from home_configuration import HomeConfiguration
from smart_home_facade import SmartHomeFacade


def capture(fn):
    buf = io.StringIO()
    with redirect_stdout(buf):
        fn()
    return buf.getvalue()


class SmartHomeTests(unittest.TestCase):
    def setUp(self):
        self.light = DeviceFactory.create("light", "Living room light")
        self.fan = DeviceFactory.create("fan", "Living room fan")
        self.door = DeviceFactory.create("door", "Main door")
        capture(self.light.turn_on)
        capture(self.fan.turn_on)

    def test_T1_factory_returns_correct_types(self):
        self.assertIsInstance(self.light, SmartLight)
        self.assertIsInstance(self.fan, SmartFan)
        self.assertIsInstance(self.door, SmartDoor)
        for d in (self.light, self.fan, self.door):
            self.assertIsInstance(d, IDevice)
        self.assertIsInstance(self.door, ILockable)
        self.assertNotIsInstance(self.light, ILockable)
        self.assertIsInstance(DeviceFactory.create("  LiGhT ", "x"), SmartLight)

    def test_T2_unsupported_type_raises(self):
        with self.assertRaises(ValueError):
            DeviceFactory.create("camera", "Cam")

    def test_T3_singleton_same_reference(self):
        self.assertIs(HomeConfiguration.instance(), HomeConfiguration.instance())
        self.assertIs(HomeConfiguration(), HomeConfiguration.instance())

    def test_T4_go_to_work(self):
        facade = SmartHomeFacade(self.light, self.fan, self.door)
        out = capture(facade.go_to_work)
        self.assertFalse(self.light.is_on)
        self.assertFalse(self.fan.is_on)
        self.assertTrue(self.door.is_locked)
        self.assertIn("Main door: LOCKED", out)

    def test_T5_go_to_sleep(self):
        capture(self.light.turn_off)
        facade = SmartHomeFacade(self.light, self.fan, self.door)
        out = capture(facade.go_to_sleep)
        self.assertFalse(self.fan.is_on)
        self.assertTrue(self.door.is_locked)
        self.assertTrue(self.light.is_on)
        level = HomeConfiguration.instance().night_light_level
        self.assertIn(f"Night light level: {level}%", out)

    def test_facade_uses_injected_config(self):
        class FakeConfig:
            night_light_level = 70

        facade = SmartHomeFacade(self.light, self.fan, self.door, config=FakeConfig())
        self.assertIn("Night light level: 70%", capture(facade.go_to_sleep))

    def test_facade_rejects_non_lockable(self):
        with self.assertRaises(TypeError):
            SmartHomeFacade(self.light, self.fan, self.fan)


if __name__ == "__main__":
    unittest.main(verbosity=2)
