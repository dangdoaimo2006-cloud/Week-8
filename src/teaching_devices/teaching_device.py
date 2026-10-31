from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Callable
from .enums import DeviceStatus, AlertSeverity
from .events import DeviceStatusChangedEventArgs, DeviceAlertEventArgs

EventHandler = Callable[[object, object], None]


class TeachingDevice(ABC):
    def __init__(self, device_id: str, name: str,
                 status: DeviceStatus = DeviceStatus.Available):
        if not device_id or not device_id.strip():
            raise ValueError("Device id khong duoc de trong")
        if not name or not name.strip():
            raise ValueError("Ten thiet bi khong duoc de trong")
        if not isinstance(status, DeviceStatus):
            raise TypeError("status phai la DeviceStatus")
        self._id, self._name, self._status = device_id, name, status
        self.__status_changed_handlers = []
        self.__alert_raised_handlers = []

    @property
    @abstractmethod
    def device_type(self):
        pass

    @property
    def id(self): return self._id

    @property
    def name(self): return self._name

    @property
    def status(self): return self._status

    def add_status_changed_handler(self, handler: EventHandler):
        if not callable(handler): raise TypeError("Handler phai la callable")
        self.__status_changed_handlers.append(handler)

    def remove_status_changed_handler(self, handler: EventHandler):
        if handler in self.__status_changed_handlers:
            self.__status_changed_handlers.remove(handler)

    def add_alert_raised_handler(self, handler: EventHandler):
        if not callable(handler): raise TypeError("Handler phai la callable")
        self.__alert_raised_handlers.append(handler)

    def remove_alert_raised_handler(self, handler: EventHandler):
        if handler in self.__alert_raised_handlers:
            self.__alert_raised_handlers.remove(handler)

    def change_status(self, new_status: DeviceStatus):
        if not isinstance(new_status, DeviceStatus):
            raise TypeError("Trang thai moi phai la DeviceStatus")
        old_status = self._status
        if old_status == new_status: return
        self._status = new_status
        args = DeviceStatusChangedEventArgs(
            self.id, old_status, new_status, datetime.now(timezone.utc))
        self._on_status_changed(args)

    def _on_status_changed(self, event_args: DeviceStatusChangedEventArgs):
        for handler in tuple(self.__status_changed_handlers):
            handler(self, event_args)

    def _raise_alert(self, message: str, severity: AlertSeverity):
        args = DeviceAlertEventArgs(
            self.id, message, severity, datetime.now(timezone.utc))
        self._on_alert_raised(args)

    def _on_alert_raised(self, event_args: DeviceAlertEventArgs):
        for handler in tuple(self.__alert_raised_handlers):
            handler(self, event_args)
