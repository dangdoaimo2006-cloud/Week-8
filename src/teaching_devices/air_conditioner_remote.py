from .teaching_device import TeachingDevice
from .enums import AlertSeverity

class AirConditionerRemote(TeachingDevice):
    def __init__(self, device_id, name, assigned_room, is_responsive=True):
        super().__init__(device_id, name)
        self.assigned_room = assigned_room
        self.is_responsive = bool(is_responsive)
        self._alert_sent = False

    def update_responsiveness(self, value):
        was_responsive = self.is_responsive
        self.is_responsive = bool(value)
        if was_responsive and not self.is_responsive and not self._alert_sent:
            self.raise_alert("Dieu khien dieu hoa khong phan hoi", AlertSeverity.Critical)
            self._alert_sent = True
        elif self.is_responsive:
            self._alert_sent = False
