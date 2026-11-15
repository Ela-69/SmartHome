import threading


class HomeConfiguration:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        # double-checked locking
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    inst = super().__new__(cls)
                    inst.home_name = "My Home"
                    inst.night_light_level = 30
                    cls._instance = inst
        return cls._instance

    @classmethod
    def instance(cls) -> "HomeConfiguration":
        return cls()

    @classmethod
    def _reset_for_tests(cls) -> None:
        with cls._lock:
            cls._instance = None
