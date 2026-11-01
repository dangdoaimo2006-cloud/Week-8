class DeviceMonitoringCoordinator:
    def __init__(self):
        self._subscriptions = []
        self._disposed = False

    def subscribe(self, device, alert_handler=None, status_handler=None):
        if self._disposed:
            raise RuntimeError("Coordinator da duoc dispose")
        if alert_handler is not None:
            self._add(device, "alert", alert_handler)
        if status_handler is not None:
            self._add(device, "status", status_handler)

    def _add(self, device, event_type, handler):
        item = (device, event_type, handler)
        if item in self._subscriptions:
            return
        if event_type == "alert":
            device.add_alert_raised_handler(handler)
        else:
            device.add_status_changed_handler(handler)
        self._subscriptions.append(item)

    def unsubscribe(self, device=None):
        remaining = []
        for subscribed_device, event_type, handler in self._subscriptions:
            if device is not None and subscribed_device is not device:
                remaining.append((subscribed_device, event_type, handler))
            elif event_type == "alert":
                subscribed_device.remove_alert_raised_handler(handler)
            else:
                subscribed_device.remove_status_changed_handler(handler)
        self._subscriptions = remaining

    def dispose(self):
        if not self._disposed:
            self.unsubscribe()
            self._disposed = True

    def __enter__(self):
        if self._disposed:
            raise RuntimeError("Coordinator da duoc dispose")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.dispose()
        return False
