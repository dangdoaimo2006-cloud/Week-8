from .enums import AlertSeverity

class ConsoleNotificationService:
    def notify(self, sender, event_args):
        print(f"[{event_args.severity.name}] {event_args.device_id}: {event_args.message}")

class MaintenanceService:
    def __init__(self):
        self.requests = []

    def handle_alert(self, sender, event_args):
        if event_args.severity == AlertSeverity.Critical:
            self.requests.append({
                "device_id": event_args.device_id,
                "message": event_args.message,
                "created_at": event_args.occurred_at,
            })

class DeviceAuditLogger:
    def __init__(self):
        self.entries = []

    def handle_status_changed(self, sender, event_args):
        self.entries.append({
            "device_id": event_args.device_id,
            "old_status": event_args.old_status,
            "new_status": event_args.new_status,
            "changed_at": event_args.changed_at,
        })

class FilteredAlertSubscriber:
    def __init__(self, alert_filter, action):
        if not callable(alert_filter) or not callable(action):
            raise TypeError("Filter va action phai la callable")
        self._alert_filter = alert_filter
        self._action = action

    def handle_alert(self, sender, event_args):
        if self._alert_filter(event_args):
            self._action(sender, event_args)
