from .teaching_device import TeachingDevice
from .enums import AlertSeverity
from .exceptions import InvalidDeviceReadingException

class WirelessMicrophone(TeachingDevice):
    def __init__(self, device_id, name, battery_level=100, signal_quality=100):
        super().__init__(device_id, name)
        self._validate(battery_level, device_id)
        self._validate(signal_quality, device_id)
        self.battery_level = battery_level
        self.signal_quality = signal_quality
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
        self._check_alert()

    def update_signal_quality(self, value):
        self._validate(value, self.id)
        self.signal_quality = value
        self._check_alert()

    def _check_alert(self):
        if self.battery_level == 0 or self.signal_quality == 0:
            zone, severity, message = "critical", AlertSeverity.Critical, "Microphone gap su co nghiem trong"
        elif self.battery_level < 30 or self.signal_quality < 40:
            zone, severity, message = "warning", AlertSeverity.Warning, "Microphone co chi so hoat dong thap"
        else:
            zone = None
        if zone is None:
            self._alert_zone = None
        elif zone != self._alert_zone:
            self.raise_alert(message, severity)
            self._alert_zone = zone
