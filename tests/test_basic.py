import unittest
from core.engine import SCABDEngine
# Using folder names with dashes requires different import style or renaming.
# Renaming folders to use underscores for better Python module compatibility.
import sys
import os
sys.path.append(os.getcwd())

from protocols.omni_shield.protocol import OmniShieldProtocol
from security.botty_guard.guard import BottyGuard

class TestSCABDFramework(unittest.TestCase):
    def test_engine_startup(self):
        engine = SCABDEngine()
        engine.startup()
        self.assertTrue(engine.is_active)
        engine.shutdown()
        self.assertFalse(engine.is_active)

    def test_omni_shield_wrap(self):
        protocol = OmniShieldProtocol()
        data = "secret"
        wrapped = protocol.wrap_data(data)
        self.assertIn("[OMNI-SHIELD-WRAPPED]", wrapped)
        self.assertIn(data, wrapped)

    def test_botty_guard_block(self):
        guard = BottyGuard()
        self.assertTrue(guard.monitor_traffic({"ip": "1.1.1.1", "content": "hello"}))
        self.assertFalse(guard.monitor_traffic({"ip": "2.2.2.2", "bot_signature": "detected"}))
        self.assertIn("2.2.2.2", guard.threat_db)

if __name__ == "__main__":
    unittest.main()
