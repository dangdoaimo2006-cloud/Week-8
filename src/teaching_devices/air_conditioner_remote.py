from .enums import AlertSeverity
from .teaching_device import TeachingDevice


class AirConditionerRemote(TeachingDevice):
    @property
    def device_type(self): return "AirConditionerRemote"

    def __init__(self, device_id: str, name: str, assigned_room: str,
                 is_responsive: bool = True):
        super().__init__(device_id, name)
        if not assigned_room or not assigned_room.strip():
            raise ValueError("Phong duoc gan khong duoc de trong")
        if not isinstance(is_responsive, bool):
            raise TypeError("is_responsive phai la bool")
        self._assigned_room = assigned_room
        self._is_responsive = is_responsive

    @property
    def assigned_room(self): return self._assigned_room

    @property
    def is_responsive(self): return self._is_responsive

    def set_responsive(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("Gia tri phan hoi phai la bool")
        was_responsive = self._is_responsive
        self._is_responsive = value
        if was_responsive and not value:
            self._raise_alert(
                f"Dieu khien dieu hoa tai phong {self.assigned_room} khong phan hoi.",
                AlertSeverity.Critical)
