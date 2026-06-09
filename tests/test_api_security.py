"""
Test script for SCABD API Security
"""
from api.endpoints import get_market_data

def test_api_access():
    print("\n--- Testing API Security Layers ---")

    # 1. Test without key
    print("[TEST] Calling API without key...")
    result, status = get_market_data(headers={})
    print(f"Result: {result} (Status Code: {status})")

    # 2. Test with invalid key
    print("\n[TEST] Calling API with INVALID key...")
    result, status = get_market_data(headers={"X-SCABD-API-KEY": "FAKE-KEY"})
    print(f"Result: {result} (Status Code: {status})")

    # 3. Test with valid key
    print("\n[TEST] Calling API with VALID key...")
    result = get_market_data(headers={"X-SCABD-API-KEY": "SCABD-PRO-2024"})
    print(f"Result: {result}")

if __name__ == "__main__":
    test_api_access()
