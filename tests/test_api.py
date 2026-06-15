import unittest
from api.main import SCABD_API

class TestSCABDAPI(unittest.TestCase):
    def setUp(self):
        self.api = SCABD_API()

    def test_get_status(self):
        status = self.api.get_status()
        self.assertEqual(status["api"], "SCABD API")
        self.assertEqual(status["status"], "online")

    def test_handle_valid_request(self):
        response = self.api.handle_request("/analyze", {})
        self.assertEqual(response["status"], "processed")
        self.assertEqual(response["endpoint"], "/analyze")

    def test_handle_invalid_request(self):
        response = self.api.handle_request("/nonexistent", {})
        self.assertEqual(response["error"], "Endpoint not found")
        self.assertEqual(response["code"], 404)

if __name__ == "__main__":
    unittest.main()
