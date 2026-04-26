#!/usr/bin/env python3
"""
Dataset Information Script
==========================
Quickly shows dataset statistics without full processing.
"""

import os

def main():
    dataset_path = "../Lung_Cancer_DataSet"

    print("=" * 60)
    print("LUNG CANCER DATASET INFORMATION")
    print("=" * 60)
    print()

    if not os.path.exists(dataset_path):
        print(f"❌ Dataset not found at: {dataset_path}")
        print("   Please ensure the dataset is in the correct location.")
        return

    categories = ["benign", "adenocarcinoma", "squamous_cell_carcinoma"]
    total = 0

    print("📊 Dataset Composition:")
    print("-" * 60)

    for cat in categories:
        cat_path = os.path.join(dataset_path, cat)
        if os.path.exists(cat_path):
            files = [f for f in os.listdir(cat_path)
                     if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif'))]
            count = len(files)
            total += count
            print(f"  {cat:40s} : {count:5d} images")
        else:
            print(f"  {cat:40s} : ❌ NOT FOUND")

    print("-" * 60)
    print(f"  {'TOTAL':40s} : {total:5d} images")
    print("=" * 60)
    print()

    print("📋 Image Format Analysis:")
    print("-" * 60)

    # Check a sample image to verify format
    sample_found = False
    for cat in categories:
        cat_path = os.path.join(dataset_path, cat)
        if os.path.exists(cat_path):
            for f in os.listdir(cat_path):
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                    print(f"  Sample from {cat}: {f}")
                    sample_found = True
                    break
        if sample_found:
            break

    if not sample_found:
        print("  ❌ No image files found")
    print("=" * 60)
    print()

    print("📝 Expected folder structure:")
    print("-" * 60)
    print("""
Lung_Cancer_DataSet/
├── benign/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── adenocarcinoma/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
└── squamous_cell_carcinoma/
    ├── image1.jpg
    ├── image2.jpg
    └── ...
""")
    print("=" * 60)
    print()

    if total > 0:
        print(f"✅ Dataset is ready! You have {total} images across 3 categories.")
        print("\nNext steps:")
        print("  1. Run: python setup.py (to check environment)")
        print("  2. Run: python lung_cancer_analysis.py")
    else:
        print("❌ No images found. Please check your dataset folder.")

if __name__ == "__main__":
    main()
