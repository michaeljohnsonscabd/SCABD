import unittest
from api.main import SCABD_API

class TestSCABDAPI(unittest.TestCase):
    def setUp(self):
        self.api = SCABD_API()

    def test_handle_request_valid_endpoint(self):
        response = self.api.handle_request("/analyze", {})
        self.assertEqual(response["status"], "processed")
        self.assertEqual(response["endpoint"], "/analyze")

    def test_handle_request_invalid_endpoint(self):
        response = self.api.handle_request("/invalid", {})
        self.assertEqual(response["error"], "Endpoint not found")
        self.assertEqual(response["code"], 404)

    def test_endpoints_is_set(self):
        self.assertIsInstance(self.api.endpoints, set)

if __name__ == "__main__":
    unittest.main()
