from enum import Enum, auto

class DeviceStatus(Enum):
    Available = auto()
    Borrowed = auto()
    UnderMaintenance = auto()

class AlertSeverity(Enum):
    Warning = auto()
    Critical = auto()
