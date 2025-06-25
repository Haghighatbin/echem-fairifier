#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test runner for EChem FAIRifier.
Provides different levels of testing with clear output.
"""
import os
import sys
import subprocess
from pathlib import Path

if os.name == "nt":
    os.system("chcp 65001 > nul")
    sys.stdout.reconfigure(encoding="utf-8")


def run_setup_test():
    """Run the basic setup test."""
    print("🔄 Running setup validation...")
    try:
        result = subprocess.run([sys.executable, "test_setup.py"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Setup test passed!")
            return True
        else:
            print("❌ Setup test failed!")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running setup test: {e}")
        return False


def run_unit_tests():
    """Run unit tests with pytest."""
    print("🔄 Running unit tests...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"],
            capture_output=True,
            text=True,
        )

        print(result.stdout)
        if result.stderr:
            print("Warnings/Errors:")
            print(result.stderr)

        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running unit tests: {e}")
        return False


def run_coverage_tests():
    """Run tests with coverage reporting."""
    print("🔄 Running tests with coverage...")
    try:
        # Install coverage if not available
        subprocess.run([sys.executable, "-m", "pip", "install", "pytest-cov"], capture_output=True)

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "tests/",
                "-v",
                "--cov=src/",
                "--cov-report=term-missing",
            ],
            capture_output=True,
            text=True,
        )

        print(result.stdout)
        if result.stderr:
            print("Warnings/Errors:")
            print(result.stderr)

        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running coverage tests: {e}")
        return False


def run_code_quality_checks():
    """Run code quality checks."""
    print("🔄 Running code quality checks...")

    checks = [
        (
            "Black formatting",
            [sys.executable, "-m", "black", "--check", "src/", "tests/", "*.py"],
        ),
        (
            "Flake8 linting",
            [sys.executable, "-m", "flake8", "src/", "--max-line-length=127"],
        ),
    ]

    all_passed = True

    for check_name, command in checks:
        try:
            print(f"  Running {check_name}...")
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"  ✅ {check_name} passed")
            else:
                print(f"  ❌ {check_name} failed")
                if result.stdout:
                    print(f"    Output: {result.stdout}")
                if result.stderr:
                    print(f"    Error: {result.stderr}")
                all_passed = False
        except FileNotFoundError:
            print(f"  ⚠️ {check_name} skipped (tool not installed)")
        except Exception as e:
            print(f"  ❌ {check_name} error: {e}")
            all_passed = False

    return all_passed


def install_dev_dependencies():
    """Install development dependencies."""
    print("🔄 Installing development dependencies...")
    dev_packages = [
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0",
        "black>=22.0.0",
        "flake8>=5.0.0",
        "mypy>=1.0.0",
    ]

    try:
        for package in dev_packages:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", package],
                capture_output=True,
                check=True,
            )
        print("✅ Development dependencies installed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def main():
    """Main test runner."""
    print("🧪 EChem FAIRifier Test Suite\n")

    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()
    else:
        print("Available test options:")
        print("  setup     - Basic setup validation")
        print("  unit      - Unit tests only")
        print("  coverage  - Tests with coverage report")
        print("  quality   - Code quality checks")
        print("  full      - All tests and checks")
        print("  install   - Install dev dependencies")
        print()
        test_type = input("Choose test type (or press Enter for 'setup'): ").lower()
        if not test_type:
            test_type = "setup"

    results = []

    if test_type in ["setup", "full"]:
        results.append(("Setup Test", run_setup_test()))

    if test_type in ["unit", "full"]:
        results.append(("Unit Tests", run_unit_tests()))

    if test_type == "coverage":
        results.append(("Coverage Tests", run_coverage_tests()))

    if test_type in ["quality", "full"]:
        results.append(("Code Quality", run_code_quality_checks()))

    if test_type == "install":
        results.append(("Install Dependencies", install_dev_dependencies()))

    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1

    print(f"\nOverall: {passed}/{total} test suites passed")

    if passed == total and total > 0:
        print("🎉 All tests passed! Ready for deployment.")
        return 0
    elif total > 0:
        print("⚠️ Some tests failed. Please review and fix issues.")
        return 1
    else:
        print("❓ No tests were run.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
