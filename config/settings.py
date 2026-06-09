"""
SCABD Configuration Settings
"""
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Project Info
PROJECT_NAME = "SCABD"
VERSION = "0.1.0"

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key-for-dev-only")

# Operational Levels
# Can be OPTIMUM, HIGH, BALANCED, LOW
OPERATIONAL_LEVEL = os.getenv("OPERATIONAL_LEVEL", "OPTIMUM")

# Future Integration Readiness
QUANTUM_READY = True
ADVANCED_COMPUTING_ADAPTER = True

# Security Enforcement
ENFORCEMENT_ENABLED = os.getenv("SCABD_ENFORCEMENT_ENABLED", "True") == "True"
LICENSE_KEY = os.getenv("SCABD_LICENSE_KEY")
