#!/usr/bin/env python3
"""
Alpine Code Assistant — entry point.

Usage:
    python3 main.py
    python3 main.py --project <name>   # skip project selector
"""

import sys
import os

# Make sure the package root is on the path when running as a script
sys.path.insert(0, os.path.dirname(__file__))

from src.cli import run

if __name__ == "__main__":
    run()
