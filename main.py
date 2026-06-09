"""
SCABD Main Entry Point
"""
import sys
from core.engine import SCABDEngine
from diagnostics.sys_check import run_all
from security.licensing import enforce_security

def main():
    # Enforce license check before anything else
    enforce_security()

    # Run internal diagnostics before starting
    run_all()

    print("Starting SCABD...")
    engine = SCABDEngine()
    engine.run()

if __name__ == "__main__":
    main()
