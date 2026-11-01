from datetime import datetime
from .enums import DeviceStatus, AlertSeverity
from .events import DeviceStatusChangedEventArgs, DeviceAlertEventArgs

class TeachingDevice:
    def __init__(self, device_id, name):
        self.id = device_id
        self.name = name
        self.status = DeviceStatus.Available
        self._status_handlers = []
        self._alert_handlers = []

    def add_status_changed_handler(self, handler):
        self._add(self._status_handlers, handler)

    def remove_status_changed_handler(self, handler):
        self._remove(self._status_handlers, handler)

    def add_alert_raised_handler(self, handler):
        self._add(self._alert_handlers, handler)

    def remove_alert_raised_handler(self, handler):
        self._remove(self._alert_handlers, handler)

    @staticmethod
    def _add(handlers, handler):
        if not callable(handler):
            raise TypeError("Event handler phai la callable")
        if handler not in handlers:
            handlers.append(handler)

    @staticmethod
    def _remove(handlers, handler):
        if handler in handlers:
            handlers.remove(handler)

    def change_status(self, new_status):
        if not isinstance(new_status, DeviceStatus):
            raise TypeError("Trang thai thiet bi khong hop le")
        if new_status == self.status:
            return
        old = self.status
        self.status = new_status
        args = DeviceStatusChangedEventArgs(self.id, old, new_status, datetime.now())
        for handler in tuple(self._status_handlers):
            handler(self, args)

    def raise_alert(self, message, severity):
        if not isinstance(severity, AlertSeverity):
            raise TypeError("Muc do canh bao khong hop le")
        args = DeviceAlertEventArgs(self.id, message, severity, datetime.now())
        for handler in tuple(self._alert_handlers):
            handler(self, args)
