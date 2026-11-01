# Class diagram

```mermaid
classDiagram
TeachingDevice <|-- ProjectorRemote
TeachingDevice <|-- AirConditionerRemote
TeachingDevice <|-- WirelessMicrophone
TeachingDevice ..> DeviceStatusChangedEventArgs
TeachingDevice ..> DeviceAlertEventArgs
DeviceMonitoringCoordinator ..> TeachingDevice
```
