from src.teaching_devices import *

def main():
    projector = ProjectorRemote("P01", "Projector Remote", 75)
    aircon = AirConditionerRemote("A01", "AC Remote", "Room 301")
    mic = WirelessMicrophone("M01", "Wireless Microphone", 80, 90)
    console = ConsoleNotificationService()
    maintenance = MaintenanceService()
    audit = DeviceAuditLogger()

    with DeviceMonitoringCoordinator() as coordinator:
        for device in (projector, aircon, mic):
            coordinator.subscribe(device, alert_handler=console.notify,
                                  status_handler=audit.handle_status_changed)
            coordinator.subscribe(device, alert_handler=maintenance.handle_alert)
        projector.update_battery(15)
        projector.update_battery(0)
        aircon.update_responsiveness(False)
        mic.update_signal_quality(25)
        mic.change_status(DeviceStatus.Borrowed)

    print("Maintenance requests:", len(maintenance.requests))
    print("Audit entries:", len(audit.entries))

if __name__ == "__main__":
    main()
