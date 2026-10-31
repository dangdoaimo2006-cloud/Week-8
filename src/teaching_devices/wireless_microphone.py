from .enums import AlertSeverity
from .teaching_device import TeachingDevice


class WirelessMicrophone(TeachingDevice):
    @property
    def device_type(self): return "WirelessMicrophone"

    def __init__(self, device_id: str, name: str,
                 battery_level: int = 100, signal_quality: int = 100):
        super().__init__(device_id, name)
        self._battery_level = self._validate_percentage(battery_level)
        self._signal_quality = self._validate_percentage(signal_quality)

    @staticmethod
    def _validate_percentage(value):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("Gia tri phan tram phai la so nguyen")
        if not 0 <= value <= 100:
            raise ValueError("Gia tri phan tram phai nam trong [0, 100]")
        return value

    @property
    def battery_level(self): return self._battery_level

    @property
    def signal_quality(self): return self._signal_quality

    @staticmethod
    def _battery_zone(value):
        if value == 0: return "critical"
        if value < 30: return "warning"
        return "normal"

    @staticmethod
    def _signal_zone(value):
        if value == 0: return "critical"
        if value < 40: return "warning"
        return "normal"

    def update_battery_level(self, value: int):
        value = self._validate_percentage(value)
        old, new = self._battery_zone(self._battery_level), self._battery_zone(value)
        self._battery_level = value
        if old == new or new == "normal": return
        if new == "critical":
            self._raise_alert("Pin micro da het (0%).", AlertSeverity.Critical)
        else:
            self._raise_alert(f"Pin micro thap: {value}%.", AlertSeverity.Warning)

    def update_signal_quality(self, value: int):
        value = self._validate_percentage(value)
        old, new = self._signal_zone(self._signal_quality), self._signal_zone(value)
        self._signal_quality = value
        if old == new or new == "normal": return
        if new == "critical":
            self._raise_alert("Tin hieu micro mat hoan toan (0%).", AlertSeverity.Critical)
        else:
            self._raise_alert(f"Chat luong tin hieu micro thap: {value}%.", AlertSeverity.Warning)
