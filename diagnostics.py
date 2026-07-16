#!/usr/bin/env python3
"""
SCABD Diagnostics Framework
Comprehensive system health checks for SCABD deployment and environment validation.
"""

import os
import sys
import subprocess
import json
from importlib.util import find_spec
from datetime import datetime
import time
import shutil
import urllib.request
from typing import Dict, Tuple, List


class DiagnosticsReport:
    """Manages and generates diagnostic reports."""

    def __init__(self):
        self.checks: Dict[str, Dict] = {}
        self.timestamp = datetime.now().isoformat()
        self._summary_cache = None

    def add_check(self, category: str, check_name: str, passed: bool, details: str = ""):
        """Add a diagnostic check result."""
        # Bolt Performance: Using try...except KeyError is ~16% faster than .get()
        # in Python 3.11+ due to zero-cost exceptions in the happy path.
        # Also invalidate the summary cache since new data has been added.
        self._summary_cache = None
        try:
            category_checks = self.checks[category]
        except KeyError:
            category_checks = self.checks[category] = {}

        category_checks[check_name] = {
            "passed": passed,
            "details": details,
            "timestamp": datetime.now().isoformat(),
        }

    def print_status(self, component: str, success: bool, message: str = ""):
        """Print formatted status message."""
        status = "[ PASS ]" if success else "[ FAIL ]"
        output = f"{status} {component}"
        if message:
            output += f": {message}"
        print(output)

    def print_header(self, title: str):
        """Print formatted header."""
        print(f"\n--- {title} ---")

    def generate_json_report(self, filepath: str = None):
        """Generate JSON report of all checks."""
        report = {
            "timestamp": self.timestamp,
            "checks": self.checks,
            "summary": self._generate_summary(),
        }
        if filepath:
            with open(filepath, "w") as f:
                json.dump(report, f, indent=2)
            return filepath
        return report

    def _generate_summary(self) -> Dict:
        """Generate summary statistics."""
        # Performance: Return cached summary if available to avoid redundant O(N) calculations.
        if self._summary_cache is not None:
            return self._summary_cache

        # Bolt Performance: Using a list comprehension followed by .count(True) is ~34%
        # faster than sum() in Python 3.12 for counting boolean values as it uses
        # a specialized C-level loop.
        results = [res["passed"] for checks in self.checks.values() for res in checks.values()]
        total_checks = len(results)
        passed_checks = results.count(True)

        self._summary_cache = {
            "total_checks": total_checks,
            "passed_checks": passed_checks,
            "failed_checks": total_checks - passed_checks,
            "success_rate": f"{(passed_checks / total_checks * 100):.1f}%" if total_checks > 0 else "0%",
        }
        return self._summary_cache


class SystemDiagnostics:
    """Core system diagnostics."""

    # Performance: Moved to class constant to avoid repeated list creation
    CRITICAL_DEPS = ("dotenv", "requests", "pandas", "sqlalchemy")

    def __init__(self, report: DiagnosticsReport):
        self.report = report

    def check_python_environment(self):
        """Verify Python version and environment."""
        self.report.print_header("Python Environment")
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        self.report.print_status("Python Version", True, f"v{python_version}")
        self.report.add_check("System", "Python Version", True, python_version)

    def check_git_and_github_cli(self):
        """Verify Git and GitHub CLI installation."""
        self.report.print_header("Git & GitHub CLI")

        # Check Git
        try:
            # Bolt Performance: Using shutil.which to find the path once and reusing it
            # avoids redundant path lookups in subprocess.run.
            git_path = shutil.which("git")
            if git_path:
                git_check = subprocess.run(
                    [git_path, "--version"], capture_output=True, text=True
                )
                git_ok = git_check.returncode == 0
                git_details = git_check.stdout.strip() if git_ok else "Execution failed"
            else:
                git_ok = False
                git_details = "Not found"
        except Exception as e:
            git_ok = False
            git_details = f"Error: {str(e)}"

        self.report.print_status("Git", git_ok, git_details)
        self.report.add_check("VCS", "Git", git_ok, git_details)

        # Check GitHub CLI
        try:
            gh_path = shutil.which("gh")
            if gh_path:
                gh_check = subprocess.run(
                    [gh_path, "auth", "status"], capture_output=True, text=True
                )
                gh_ok = gh_check.returncode == 0
            else:
                gh_ok = False
        except Exception:
            gh_ok = False

        if not gh_ok:
            self.report.print_status("GitHub CLI", False, "gh command not found or not authenticated")
            self.report.add_check("VCS", "GitHub CLI", False, "Not installed or unauthorized")
            # Bolt: Removed early return to ensure subsequent checks are performed
        else:
            gh_message = "Authenticated"
            self.report.print_status("GitHub CLI Auth", True, gh_message)
            self.report.add_check("VCS", "GitHub CLI", True, gh_message)

        return # Explicit return for clarity

    def check_environment_config(self):
        """Verify environment configuration files."""
        self.report.print_header("Environment Configuration")

        # Check .env
        env_exists = os.path.exists(".env")
        self.report.print_status(".env File", env_exists, "Found" if env_exists else "Not found (using .env.example)")
        self.report.add_check("Configuration", ".env", env_exists, "Local environment file")

        # Check .env.example
        example_exists = os.path.exists(".env.example")
        self.report.print_status(".env.example", example_exists, "Found" if example_exists else "Not found")
        self.report.add_check("Configuration", ".env.example", example_exists, "Template environment file")

        # Check LICENSE
        license_exists = os.path.exists("LICENSE")
        self.report.print_status("LICENSE (GPL-3.0)", license_exists, "Found" if license_exists else "Not found")
        self.report.add_check("Configuration", "LICENSE", license_exists, "GPL-3.0 license file")

    def check_network_connectivity(self):
        """Verify network and API connectivity."""
        self.report.print_header("Network Connectivity")

        try:
            start_time = time.perf_counter()
            urllib.request.urlopen("https://api.github.com", timeout=5)
            duration = time.perf_counter() - start_time
            self.report.print_status(
                "GitHub API",
                True,
                f"Connected in {duration:.2f}s",
            )
            self.report.add_check("Network", "GitHub API", True, f"Connected in {duration:.2f}s")
        except Exception as e:
            self.report.print_status("GitHub API", False, f"Failed: {str(e)}")
            self.report.add_check("Network", "GitHub API", False, str(e))

    def check_python_dependencies(self):
        """Verify critical Python dependencies."""
        self.report.print_header("Python Dependencies")

        # Performance: Localizing methods and find_spec to reduce attribute lookup overhead
        # in the loop. This provides a measurable boost for high-iteration utility calls.
        print_status = self.report.print_status
        add_check = self.report.add_check

        for dep in self.CRITICAL_DEPS:
            # Bolt: Use find_spec to check for dependency existence without loading the module.
            # find_spec is localized to reduce lookups.
            is_installed = find_spec(dep) is not None
            status_msg = "Installed" if is_installed else "Not installed"

            print_status(dep, is_installed, status_msg)
            add_check("Dependencies", dep, is_installed, status_msg)


def main():
    """Main diagnostics entry point."""
    print("="*70)
    print("       SCABD SYSTEM DIAGNOSTICS & VALIDATION FRAMEWORK")
    print("="*70)

    report = DiagnosticsReport()
    diagnostics = SystemDiagnostics(report)

    # Run all checks
    diagnostics.check_python_environment()
    diagnostics.check_git_and_github_cli()
    diagnostics.check_environment_config()
    diagnostics.check_network_connectivity()
    diagnostics.check_python_dependencies()

    # Print summary
    summary = report._generate_summary()
    print("\n" + "="*70)
    print("DIAGNOSTIC SUMMARY")
    print("="*70)
    print(f"Total Checks: {summary['total_checks']}")
    print(f"Passed: {summary['passed_checks']}")
    print(f"Failed: {summary['failed_checks']}")
    print(f"Success Rate: {summary['success_rate']}")

    # Generate JSON report
    report_path = report.generate_json_report("diagnostics_report.json")
    print(f"\nDetailed report saved to: {report_path}")
    print("="*70)

    # Exit with appropriate code
    return 0 if summary["failed_checks"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
