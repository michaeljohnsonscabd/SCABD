"""
SCABD Adaptive Controller
Manages system performance levels based on telemetry.
"""
import time

class AdaptiveController:
    def __init__(self, engine):
        self.engine = engine
        self.last_adjustment = time.time()

    def evaluate_performance(self, metrics):
        """
        Adjusts engine operational levels based on system metrics.
        metrics: dict containing 'cpu_usage' and 'memory_usage'
        """
        cpu = metrics.get('cpu_usage', 0)
        mem = metrics.get('memory_usage', 0)

        if cpu > 85 or mem > 85:
            if self.engine.level != "LEAN":
                print(f"[ADAPTIVE] High resource usage detected (CPU: {cpu}%, MEM: {mem}%). Switching to LEAN mode.")
                self.engine.level = "LEAN"
        elif cpu < 50 and mem < 50:
            if self.engine.level != "OPTIMUM":
                print(f"[ADAPTIVE] Resources available (CPU: {cpu}%, MEM: {mem}%). Switching to OPTIMUM mode.")
                self.engine.level = "OPTIMUM"

        self.last_adjustment = time.time()
