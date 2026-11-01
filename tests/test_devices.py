import unittest
from src.teaching_devices import *

class DeviceTests(unittest.TestCase):
    def test_projector_thresholds(self):
        d = ProjectorRemote("P1", "Projector")
        events = []
        d.add_alert_raised_handler(lambda s, e: events.append(e))
        d.update_battery(15)
        d.update_battery(10)
        d.update_battery(0)
        d.update_battery(0)
        self.assertEqual(len(events), 2)
        self.assertEqual(events[-1].severity, AlertSeverity.Critical)

    def test_aircon(self):
        d = AirConditionerRemote("A1", "AC", "Room 1")
        events = []
        d.add_alert_raised_handler(lambda s, e: events.append(e))
        d.update_responsiveness(False)
        d.update_responsiveness(False)
        self.assertEqual(len(events), 1)

    def test_microphone(self):
        d = WirelessMicrophone("M1", "Mic")
        events = []
        d.add_alert_raised_handler(lambda s, e: events.append(e))
        d.update_signal_quality(30)
        d.update_signal_quality(0)
        self.assertEqual(len(events), 2)

if __name__ == "__main__":
    unittest.main()
