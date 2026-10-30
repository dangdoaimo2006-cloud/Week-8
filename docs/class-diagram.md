# So do lop - Week 8

```mermaid
classDiagram
    class TeachingDevice {
        <<abstract>>
        +id
        +name
        +status
        +change_status(new_status)
        +subscribe_status_changed(handler)
        +unsubscribe_status_changed(handler)
        +subscribe_alert_raised(handler)
        +unsubscribe_alert_raised(handler)
        #raise_alert(message, severity)
    }
    class ProjectorRemote {
        +battery_level
        +update_battery_level(new_level)
    }
    class AirConditionerRemote {
        +assigned_room
        +is_responsive
        +update_response_state(is_responsive)
    }
    class WirelessMicrophone {
        +battery_level
        +signal_quality
        +update_battery_level(new_level)
        +update_signal_quality(new_quality)
    }
    class DeviceStatusChangedEventArgs {
        +device_id
        +old_status
        +new_status
        +changed_at
    }
    class DeviceAlertEventArgs {
        +device_id
        +message
        +severity
        +occurred_at
    }
    class ConsoleNotificationService {
        +handle_alert(sender, event_args)
    }
    class DeviceAuditLogger {
        +entries
        +handle_status_changed(sender, event_args)
    }
    class MaintenanceService {
        +requests
        +handle_critical_alert(sender, event_args)
    }
    class FilteredAlertSubscriber {
        -filter
        -action
        +handle_alert(sender, event_args)
    }
    class DeviceMonitoringCoordinator {
        +subscribe()
        +unsubscribe()
        +dispose()
    }
    TeachingDevice <|-- ProjectorRemote
    TeachingDevice <|-- AirConditionerRemote
    TeachingDevice <|-- WirelessMicrophone
    TeachingDevice ..> DeviceStatusChangedEventArgs : publishes
    TeachingDevice ..> DeviceAlertEventArgs : publishes
    DeviceMonitoringCoordinator o-- TeachingDevice : manages
    DeviceMonitoringCoordinator --> ConsoleNotificationService
    DeviceMonitoringCoordinator --> DeviceAuditLogger
    DeviceMonitoringCoordinator --> MaintenanceService
    ConsoleNotificationService ..> DeviceAlertEventArgs : handles
    DeviceAuditLogger ..> DeviceStatusChangedEventArgs : handles
    MaintenanceService ..> DeviceAlertEventArgs : handles
    FilteredAlertSubscriber ..> DeviceAlertEventArgs : filters
```

## Ghi chu
- Ba loai thiet bi ke thua `TeachingDevice`.
- Publisher khong phu thuoc vao subscriber cu the.
- Coordinator tap trung viec dang ky va huy dang ky handler.
- `FilteredAlertSubscriber` nhan hai callable: ham loc va ham hanh dong.
