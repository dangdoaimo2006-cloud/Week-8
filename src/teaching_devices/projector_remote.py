from .teaching_device import TeachingDevice
from .enums import AlertSeverity
from .exceptions import InvalidDeviceReadingException


class ProjectorRemote(TeachingDevice):
    def __init__(self, device_id, name, battery_level=100):
        super().__init__(device_id, name)

        self._validate_percentage(battery_level, device_id)

        self.battery_level = battery_level
        self._last_alert_zone = None

    @staticmethod
    def _validate_percentage(value, device_id):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("Gia tri phan tram phai la so nguyen")

        if value < 0 or value > 100:
            raise InvalidDeviceReadingException(device_id, value)

    def update_battery(self, battery_level):
        self._validate_percentage(battery_level, self.id)

        self.battery_level = battery_level

        if battery_level == 0:
            current_zone = "critical"
            severity = AlertSeverity.Critical
            message = "Pin dieu khien may chieu da het"

        elif battery_level < 20:
            current_zone = "warning"
            severity = AlertSeverity.Warning
            message = "Pin dieu khien may chieu sap het"

        else:
            current_zone = None

        if current_zone is None:
            self._last_alert_zone = None
            return

        if current_zone != self._last_alert_zone:
            self.raise_alert(message, severity)
            self._last_alert_zone = current_zone