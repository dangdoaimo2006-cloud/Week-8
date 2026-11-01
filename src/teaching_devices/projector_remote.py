from .teaching_device import TeachingDevice
from .enums import AlertSeverity
from .exceptions import InvalidDeviceReadingException

class ProjectorRemote(TeachingDevice):
    def __init__(self, device_id, name, battery_level=100):
        super().__init__(device_id, name)
        self._validate(battery_level, device_id)
        self.battery_level = battery_level
        self._alert_zone = None

    @staticmethod
    def _validate(value, device_id):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("Gia tri phan tram phai la so nguyen")
        if not 0 <= value <= 100:
            raise InvalidDeviceReadingException(device_id, value)

    def update_battery(self, value):
        self._validate(value, self.id)
        self.battery_level = value
        if value == 0:
            zone, severity, message = "critical", AlertSeverity.Critical, "Pin dieu khien may chieu da het"
        elif value < 20:
            zone, severity, message = "warning", AlertSeverity.Warning, "Pin dieu khien may chieu sap het"
        else:
            zone = None
        if zone is None:
            self._alert_zone = None
        elif zone != self._alert_zone:
            self.raise_alert(message, severity)
            self._alert_zone = zone
