#!/usr/bin/env python3
"""
Jules Environment Diagnostic & Integration Tester
Verifies core GNU tools, GitHub CLI state, environment variables, and secure connectivity.
"""

import os
import subprocess
import sys
import time
import shutil
import urllib.request


def print_status(component, success, message=""):
    status = "[ PASS ]" if success else "[ FAIL ]"
    print(f"{status} {component}: {message}")


def check_gnu_and_cli():
    print("--- Checking System Utilities & GitHub CLI ---")

    # Test Git existence
    # Bolt Performance: Using shutil.which to find the path once and reusing it
    # avoids redundant path lookups in subprocess.run.
    try:
        git_path = shutil.which("git")
        if git_path:
            git_check = subprocess.run(
                [git_path, "--version"], capture_output=True, text=True
            )
            print_status("Git Core", git_check.returncode == 0, git_check.stdout.strip())
        else:
            print_status("Git Core", False, "git command not found")
    except Exception as e:
        print_status("Git Core", False, f"Error: {e}")

    # Test GitHub CLI auth status
    try:
        gh_path = shutil.which("gh")
        if gh_path:
            gh_check = subprocess.run(
                [gh_path, "auth", "status"], capture_output=True, text=True
            )
            # gh auth status returns 0 if logged in, non-zero if not
            is_gh_authed = gh_check.returncode == 0
        else:
            is_gh_authed = False
            print_status("GitHub CLI", False, "gh command not found.")
    except Exception:
        is_gh_authed = False
        print_status("GitHub CLI", False, "Error checking gh status.")

    gh_message = (
        "Authenticated successfully."
        if is_gh_authed
        else "Not authenticated. Run 'gh auth login' inside the box."
    )
    print_status("GitHub CLI Auth", is_gh_authed, gh_message)
    return is_gh_authed


def check_environment_files():
    print("\n--- Verifying Core Architecture Files ---")

    # Check for .env file
    env_exists = os.path.exists(".env")
    if env_exists:
        print_status(".env Configuration", True, "Found local environment file.")
    else:
        # Check if they at least have the template
        example_exists = os.path.exists(".env.example")
        msg = (
            "Missing .env file. (.env.example is present)"
            if example_exists
            else "Missing both .env and .env.example."
        )
        print_status(".env Configuration", False, msg)

    # Check for GNU GPL-3.0 License
    license_exists = os.path.exists("LICENSE")
    print_status(
        "GPL-3.0 License File", license_exists, "Found" if license_exists else "Missing"
    )


def test_network_and_webhooks():
    print("\n--- Testing API & Secure Connectivity ---")
    # Simulate a lightweight ping to verify DNS and basic outbound internet translation
    try:
        start_time = time.perf_counter()
        # Using a reliable public standard API to verify handshake
        urllib.request.urlopen("https://api.github.com", timeout=5)
        duration = time.perf_counter() - start_time
        print_status(
            "Outbound Network Handshake",
            True,
            f"Connected to api.github.com in {duration:.2f}s",
        )
    except Exception as e:
        print_status("Outbound Network Handshake", False, f"Connection failed: {e}")


if __name__ == "__main__":
    print("==================================================================")
    print("      LAUNCHING JULES ENVIRONMENT INTEGRATION DIAGNOSTIC          ")
    print("==================================================================")

    cli_ok = check_gnu_and_cli()
    check_environment_files()
    test_network_and_webhooks()

    print("==================================================================")
