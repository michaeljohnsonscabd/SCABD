# Standard GNU GPL v3.0 License Header
# This file is part of SCABD.

class Engine:
    """
    Core SCABD processing engine.
    """
    def __init__(self):
        self.status = "Idle"

    def start(self):
        self.status = "Running"
        print("SCABD Engine Started.")
