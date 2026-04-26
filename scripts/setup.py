#!/usr/bin/env python3
"""
Quick Setup and Test Script
===========================
This script checks your environment and installs dependencies.
"""

import sys
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        return False

    print("✅ Python version OK")
    return True

def check_module(module_name, pip_name=None):
    """Check if a module is installed."""
    if pip_name is None:
        pip_name = module_name

    spec = importlib.util.find_spec(module_name)
    if spec is None:
        print(f"❌ {module_name} is NOT installed")
        print(f"   Install with: pip install {pip_name}")
        return False
    else:
        print(f"✅ {module_name} is installed")
        return True

def install_dependencies():
    """Install all dependencies from requirements.txt."""
    print("\n" + "="*50)
    print("Installing dependencies...")
    print("="*50)

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        return False

def test_dataset():
    """Check if dataset is accessible."""
    print("\n" + "="*50)
    print("Checking dataset...")
    print("="*50)

    import os

    dataset_path = "Lung_Cancer_DataSet"

    if not os.path.exists(dataset_path):
        print(f"❌ Dataset folder '{dataset_path}' not found!")
        print("   Please make sure your dataset is in the correct location.")
        return False

    categories = ["benign", "adenocarcinoma", "squamous_cell_carcinoma"]
    all_good = True

    for cat in categories:
        cat_path = os.path.join(dataset_path, cat)
        if os.path.exists(cat_path):
            count = len([f for f in os.listdir(cat_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))])
            print(f"✅ {cat}: {count} images")
        else:
            print(f"❌ {cat}: folder not found")
            all_good = False

    if all_good:
        print("✅ Dataset structure is correct!")

    return all_good

def main():
    print("="*50)
    print("LUNG CANCER IMAGE ANALYSIS - SETUP TEST")
    print("="*50)
    print()

    # Check Python
    python_ok = check_python_version()
    print()

    # Check modules
    print("Checking required modules...")
    modules = [
        ("cv2", "opencv-python"),
        ("numpy", "numpy"),
        ("matplotlib", "matplotlib")
    ]

    modules_ok = True
    for module, pip_name in modules:
        if not check_module(module, pip_name):
            modules_ok = False
    print()

    # Offer to install
    if not modules_ok:
        response = input("Would you like to install missing dependencies? (y/n): ").lower().strip()
        if response == 'y':
            install_ok = install_dependencies()
            if install_ok:
                print("\n✅ Dependencies installed. Please re-run this script to verify.")
        else:
            print("⚠️  Please install dependencies manually before running the main script.")
    else:
        print("✅ All required modules are installed!")

    # Test dataset
    dataset_ok = test_dataset()
    print()

    # Final summary
    print("="*50)
    print("SUMMARY")
    print("="*50)

    if python_ok and modules_ok and dataset_ok:
        print("✅ Everything is ready!")
        print("\nYou can now run:")
        print("  python lung_cancer_analysis.py")
        print("\nHave fun analyzing lung cancer images! 🩺")
    else:
        print("❌ Some issues need to be resolved before running the main script.")
        print("\nPlease fix the errors above and try again.")

if __name__ == "__main__":
    main()
