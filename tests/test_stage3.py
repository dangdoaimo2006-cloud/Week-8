import unittest
from src.teaching_devices import *

class Stage3Tests(unittest.TestCase):
    def test_maintenance_critical_only(self):
        d = ProjectorRemote("P1", "Projector")
        service = MaintenanceService()
        d.add_alert_raised_handler(service.handle_alert)
        d.update_battery(15)
        self.assertEqual(len(service.requests), 0)
        d.update_battery(0)
        self.assertEqual(len(service.requests), 1)

    def test_filtered_subscriber(self):
        d = ProjectorRemote("P2", "Projector")
        got = []
        sub = FilteredAlertSubscriber(
            lambda e: e.severity == AlertSeverity.Critical,
            lambda s, e: got.append(e),
        )
        d.add_alert_raised_handler(sub.handle_alert)
        d.update_battery(0)
        self.assertEqual(len(got), 1)

    def test_coordinator_dispose_and_duplicate(self):
        d = ProjectorRemote("P3", "Projector")
        service = MaintenanceService()
        c = DeviceMonitoringCoordinator()
        c.subscribe(d, alert_handler=service.handle_alert)
        c.subscribe(d, alert_handler=service.handle_alert)
        c.dispose()
        d.update_battery(0)
        self.assertEqual(len(service.requests), 0)

    def test_custom_exception(self):
        with self.assertRaises(InvalidDeviceReadingException):
            ProjectorRemote("P4", "Projector", 101)

if __name__ == "__main__":
    unittest.main()
