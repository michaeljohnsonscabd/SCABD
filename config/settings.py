# Standard GNU GPL v3.0 License Header
# This file is part of SCABD.

import os

class Settings:
    """
    SCABD System Settings.
    """
    def __init__(self):
        self.app_name = "SCABD"
        self.debug = os.getenv("DEBUG", "False") == "True"
