#!/usr/bin/env python3
"""
Entry point for EChem FAIRifier Streamlit application.
Run this file to start the application.
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

# Import and run the main app
from echem_fairifier.app import main

if __name__ == "__main__":
    main()
