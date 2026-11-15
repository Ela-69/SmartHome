from device_factory import DeviceFactory
from home_configuration import HomeConfiguration
from smart_home_facade import SmartHomeFacade

light = DeviceFactory.create("light", "Living room light")
fan = DeviceFactory.create("FAN ", "Living room fan")
door = DeviceFactory.create("door", "Main door")

c1, c2 = HomeConfiguration.instance(), HomeConfiguration.instance()
if c1 is not c2:
    raise Exception("Singleton implementation is incorrect.")
print("Same config instance:", c1 is c2)

facade = SmartHomeFacade(light, fan, door)
print("--- GoToWork ---")
facade.go_to_work()
print("--- GoToSleep ---")
facade.go_to_sleep()
print("--- Direct control ---")
light.turn_on()

try:
    DeviceFactory.create("camera", "Cam 1")
except ValueError as e:
    print("Error:", e)
