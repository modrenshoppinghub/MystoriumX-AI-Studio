"""
Pytest configuration file to dynamically inject root path into sys.path.
"""
import sys
from pathlib import Path

# Add project root directory to sys.path
root_dir = Path(__file__).parent.parent.resolve()
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
