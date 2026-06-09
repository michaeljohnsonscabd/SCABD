"""
SCABD Licensing and Security Enforcement
"""
import hashlib
import os
import platform
import sys

class LicenseManager:
    def __init__(self):
        self.license_key = os.getenv("SCABD_LICENSE_KEY")
        self.enforcement_enabled = os.getenv("SCABD_ENFORCEMENT_ENABLED", "True") == "True"

    def get_server_fingerprint(self):
        """Generates a unique fingerprint for the current server."""
        node = platform.node()
        system = platform.system()
        version = platform.version()
        machine = platform.machine()
        processor = platform.processor()

        raw_id = f"{node}-{system}-{version}-{machine}-{processor}"
        return hashlib.sha256(raw_id.encode()).hexdigest()

    def validate_license(self):
        """
        Validates the current license key against the server fingerprint.
        In a production environment, this would call a remote auth server.
        For now, we implement a 'Demo' mode and a strict mode.
        """
        if not self.enforcement_enabled:
            print("[WARNING] License enforcement is DISABLED. System is vulnerable.")
            return True

        if not self.license_key:
            print("[CRITICAL] Missing SCABD_LICENSE_KEY in environment.")
            return False

        # Simplified validation for demo purposes
        # A real implementation would verify the key with an external source or a signed blob
        fingerprint = self.get_server_fingerprint()

        # Example: A valid key could be the hash of the fingerprint + a secret salt
        # For the user, we will allow a special 'DEVELOPER-TRIAL' key for now
        if self.license_key == "DEVELOPER-TRIAL":
            print(f"[AUTH] Validated Developer Trial License for fingerprint: {fingerprint}")
            return True

        print(f"[ERROR] Invalid License Key for fingerprint: {fingerprint}")
        return False

def enforce_security():
    manager = LicenseManager()
    if not manager.validate_license():
        print("**************************************************")
        print("   UNAUTHORIZED ACCESS DETECTED - SYSTEM HALTED")
        print("   Please contact support to obtain a license.")
        print("**************************************************")
        sys.exit(1)
