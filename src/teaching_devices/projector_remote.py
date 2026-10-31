from .enums import AlertSeverity
from .teaching_device import TeachingDevice


class ProjectorRemote(TeachingDevice):
    @property
    def device_type(self): return "ProjectorRemote"

    def __init__(self, device_id: str, name: str, battery_level: int = 100):
        super().__init__(device_id, name)
        self._battery_level = self._validate_percentage(battery_level)

    @staticmethod
    def _validate_percentage(value):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("Muc pin phai la so nguyen")
        if not 0 <= value <= 100:
            raise ValueError("Muc pin phai nam trong [0, 100]")
        return value

    @property
    def battery_level(self): return self._battery_level

    @staticmethod
    def _zone(value):
        if value == 0: return "critical"
        if value < 20: return "warning"
        return "normal"

    def update_battery_level(self, value: int):
        value = self._validate_percentage(value)
        old_zone, new_zone = self._zone(self._battery_level), self._zone(value)
        self._battery_level = value
        if old_zone == new_zone or new_zone == "normal": return
        if new_zone == "critical":
            self._raise_alert("Pin dieu khien may chieu da het (0%).", AlertSeverity.Critical)
        else:
            self._raise_alert(f"Pin dieu khien may chieu thap: {value}%.", AlertSeverity.Warning)
