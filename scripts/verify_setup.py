#!/usr/bin/env python3
"""
Verify Setup Script for Task 1.1

This script checks that your development environment is properly configured
and generates a verification token to submit via the web portal.

Usage:
    python scripts/verify_setup.py
"""

import hashlib
import platform
import subprocess
import sys
from datetime import datetime


def check_python_version():
    """Check Python version is 3.8+."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        return False, f"Python {version.major}.{version.minor} (need 3.8+)"
    return True, f"Python {version.major}.{version.minor}.{version.micro}"


def check_package_installed(package_name):
    """Check if a package is installed."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", package_name],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            # Extract version from pip show output
            for line in result.stdout.split("\n"):
                if line.startswith("Version:"):
                    version = line.split(":")[1].strip()
                    return True, version
        return False, "not installed"
    except Exception as e:
        return False, str(e)


def check_git_configured():
    """Check if git is configured with user name and email."""
    try:
        name_result = subprocess.run(
            ["git", "config", "user.name"],
            capture_output=True,
            text=True,
        )
        email_result = subprocess.run(
            ["git", "config", "user.email"],
            capture_output=True,
            text=True,
        )

        name = name_result.stdout.strip()
        email = email_result.stdout.strip()

        if name and email:
            return True, f"{name} <{email}>"
        return False, "Git user.name or user.email not set"
    except Exception:
        return False, "Git not found"


def generate_token(checks_passed):
    """Generate a verification token based on environment."""
    # Create a hash based on machine info and timestamp
    data = f"{platform.node()}-{platform.system()}-{datetime.now().strftime('%Y%m%d')}"
    hash_value = hashlib.sha256(data.encode()).hexdigest()[:12].upper()

    # Format: CARTLY-{hash}-{checksum}
    checksum = hashlib.md5(hash_value.encode()).hexdigest()[:4].upper()

    return f"CARTLY-{hash_value}-{checksum}"


def main():
    print("=" * 60)
    print("  Cartly Virtual Internship - Environment Verification")
    print("=" * 60)
    print()

    checks = []
    all_passed = True

    # Check Python version
    passed, info = check_python_version()
    checks.append(("Python Version", passed, info))
    if not passed:
        all_passed = False

    # Check required packages
    required_packages = ["pandas", "numpy", "pytest"]
    for package in required_packages:
        passed, version = check_package_installed(package)
        checks.append((f"Package: {package}", passed, version))
        if not passed:
            all_passed = False

    # Check git configuration
    passed, info = check_git_configured()
    checks.append(("Git Configuration", passed, info))
    if not passed:
        all_passed = False

    # Print results
    print("Environment Checks:")
    print("-" * 60)

    for name, passed, info in checks:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {status} {name}: {info}")

    print()
    print("-" * 60)

    if all_passed:
        token = generate_token(checks)
        print()
        print("  All checks passed!")
        print()
        print("  Your verification token:")
        print()
        print(f"    {token}")
        print()
        print("  Submit this token using the web portal:")
        print("    Web portal: Go to Task 1.1 and enter the token")
        print()
        print("=" * 60)
        return 0
    else:
        print()
        print("  Some checks failed. Please fix the issues above and try again.")
        print()
        print("  Common fixes:")
        print("    - Python version: Install Python 3.8 or higher")
        print("    - Missing packages: Run 'pip install -r requirements.txt'")
        print("    - Git config: Run 'git config user.name \"Your Name\"'")
        print("                  Run 'git config user.email \"your@email.com\"'")
        print()
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
