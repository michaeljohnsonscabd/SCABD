import unittest
from security.botty_guard.guard import BottyGuard

class TestBottyGuard(unittest.TestCase):
    def setUp(self):
        self.guard = BottyGuard()

    def test_monitor_traffic_allowed(self):
        traffic_data = {"ip": "1.1.1.1"}
        self.assertTrue(self.guard.monitor_traffic(traffic_data))

    def test_monitor_traffic_blocked_ip(self):
        ip = "1.2.3.4"
        self.guard.block_threat(ip)
        traffic_data = {"ip": ip}
        self.assertFalse(self.guard.monitor_traffic(traffic_data))

    def test_monitor_traffic_bot_signature(self):
        traffic_data = {"ip": "2.2.2.2", "bot_signature": "bad-bot"}
        self.assertFalse(self.guard.monitor_traffic(traffic_data))
        self.assertIn("2.2.2.2", self.guard.threat_db)

    def test_monitor_traffic_no_ip(self):
        traffic_data = {"bot_signature": "bad-bot"}
        self.assertFalse(self.guard.monitor_traffic(traffic_data))
        self.assertEqual(len(self.guard.threat_db), 0)

    def test_monitor_traffic_empty_data(self):
        traffic_data = {}
        self.assertTrue(self.guard.monitor_traffic(traffic_data))

if __name__ == "__main__":
    unittest.main()
