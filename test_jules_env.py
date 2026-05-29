#!/usr/bin/env python3
import os
import subprocess
import sys

def print_status(component, success, message=""):
    status = "[ PASS ]" if success else "[ FAIL ]"
    print(f"{status} {component}: {message}")

if __name__ == "__main__":
    print("==================================================================")
    print("      LAUNCHING JULES ENVIRONMENT INTEGRATION DIAGNOSTIC          ")
    print("==================================================================")

    git_check = subprocess.run(["git", "--version"], capture_output=True, text=True)
    print_status("Git Core", git_check.returncode == 0, git_check.stdout.strip())

    env_exists = os.path.exists(".env")
    print_status(".env Configuration", env_exists, "Found local environment." if env_exists else "Missing .env")

    license_exists = os.path.exists("LICENSE")
    print_status("GPL-3.0 License File", license_exists, "Found" if license_exists else "Missing")
    print("==================================================================")
