from .teaching_device import TeachingDevice
from .enums import AlertSeverity
from .exceptions import InvalidDeviceReadingException


class WirelessMicrophone(TeachingDevice):
    def __init__(
        self,
        device_id,
        name,
        battery_level=100,
        signal_quality=100
    ):
        super().__init__(device_id, name)

        self._validate_percentage(battery_level, device_id)
        self._validate_percentage(signal_quality, device_id)

        self.battery_level = battery_level
        self.signal_quality = signal_quality

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
        self._check_alert()

    def update_signal_quality(self, signal_quality):
        self._validate_percentage(signal_quality, self.id)

        self.signal_quality = signal_quality
        self._check_alert()

    def _check_alert(self):
        if self.battery_level == 0 or self.signal_quality == 0:
            current_zone = "critical"
            severity = AlertSeverity.Critical
            message = "Microphone gap su co nghiem trong"

        elif self.battery_level < 30 or self.signal_quality < 40:
            current_zone = "warning"
            severity = AlertSeverity.Warning
            message = "Microphone co chi so hoat dong thap"

        else:
            current_zone = None

        if current_zone is None:
            self._last_alert_zone = None
            return

        if current_zone != self._last_alert_zone:
            self.raise_alert(message, severity)
            self._last_alert_zone = current_zone