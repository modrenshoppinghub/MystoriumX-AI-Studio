"""
Automated Test Suite Runner for MystoriumX AI Studio.
Provides execution verification for local and production deployment pipelines.
"""

import sys
import pytest

def main():
    print("=" * 60)
    print(" MystoriumX AI Studio v1.0 - Automated Test Runner")
    print("=" * 60)
    
    args = [
        "-v",
        "--tb=short",
        "tests/"
    ]
    
    exit_code = pytest.main(args)
    if exit_code == 0:
        print("\nSUCCESS: All unit and integration tests passed.")
    else:
        print(f"\nFAILURE: Test suite failed with exit code {exit_code}.")
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
