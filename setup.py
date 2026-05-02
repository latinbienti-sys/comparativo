#!/usr/bin/env python3
"""
Setup script for Price Comparator System
"""

import os
import sys

def setup():
    print("Setting up Price Comparator System...")
    
    # Create data directory
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"✓ Created {data_dir}/ directory")
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("✗ Python 3.7 or higher is required")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Check/install dependencies
    print("\nChecking dependencies...")
    dependencies = ['requests', 'beautifulsoup4', 'lxml']
    
    missing = []
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"  ✓ {dep}")
        except ImportError:
            missing.append(dep)
            print(f"  ✗ {dep} (not installed)")
    
    if missing:
        print(f"\nInstalling missing dependencies: {', '.join(missing)}")
        os.system(f"pip install {' '.join(missing)}")
    
    print("\n✓ Setup completed!")
    print("\nRun the system with: python main.py")

if __name__ == "__main__":
    setup()
