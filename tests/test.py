import unittest

from src.teaching_devices import (
    ProjectorRemote,
    WirelessMicrophone,
    AlertSeverity,
    MaintenanceService,
    DeviceAuditLogger,
    FilteredAlertSubscriber,
    DeviceMonitoringCoordinator,
    InvalidDeviceReadingException
)


class Stage3Tests(unittest.TestCase):

    def test_maintenance_only_receives_critical_alert(self):
        device = ProjectorRemote("P01", "Projector Remote")
        service = MaintenanceService()

        device.add_alert_raised_handler(service.handle_alert)

        device.update_battery(15)
        self.assertEqual(len(service.requests), 0)

        device.update_battery(0)
        self.assertEqual(len(service.requests), 1)

    def test_filtered_alert_subscriber(self):
        device = ProjectorRemote("P02", "Projector Remote")
        received = []

        subscriber = FilteredAlertSubscriber(
            lambda event: event.severity == AlertSeverity.Critical,
            lambda sender, event: received.append(event)
        )

        device.add_alert_raised_handler(subscriber.handle_alert)

        device.update_battery(10)
        device.update_battery(0)

        self.assertEqual(len(received), 1)
        self.assertEqual(
            received[0].severity,
            AlertSeverity.Critical
        )

    def test_audit_logger(self):
        device = ProjectorRemote("P03", "Projector Remote")
        logger = DeviceAuditLogger()

        device.add_status_changed_handler(
            logger.handle_status_changed
        )

        device.change_status(device.status.Borrowed)

        self.assertEqual(len(logger.entries), 1)

    def test_coordinator_prevents_duplicate_subscription(self):
        device = ProjectorRemote("P04", "Projector Remote")
        service = MaintenanceService()
        coordinator = DeviceMonitoringCoordinator()

        coordinator.subscribe(
            device,
            alert_handler=service.handle_alert
        )

        coordinator.subscribe(
            device,
            alert_handler=service.handle_alert
        )

        device.update_battery(0)

        self.assertEqual(len(service.requests), 1)

    def test_coordinator_dispose(self):
        device = ProjectorRemote("P05", "Projector Remote")
        service = MaintenanceService()
        coordinator = DeviceMonitoringCoordinator()

        coordinator.subscribe(
            device,
            alert_handler=service.handle_alert
        )

        coordinator.dispose()
        device.update_battery(0)

        self.assertEqual(len(service.requests), 0)

    def test_invalid_device_reading(self):
        with self.assertRaises(InvalidDeviceReadingException):
            ProjectorRemote("P06", "Projector Remote", 120)

        with self.assertRaises(InvalidDeviceReadingException):
            WirelessMicrophone(
                "M01",
                "Microphone",
                battery_level=100,
                signal_quality=-1
            )


if __name__ == "__main__":
    unittest.main()