"""
Lung Cancer Image Analysis - Digital Image Processing Project
=============================================================
This script performs image analysis on lung cancer datasets with three categories:
- benign
- adenocarcinoma
- squamous_cell_carcinoma

Steps:
1. Load dataset
2. Display sample images
3. Preprocessing (grayscale, blur)
4. Segmentation (Otsu thresholding)
5. Circular cell detection using contours
6. Pseudo-coloring
7. Visualization of results
"""

import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend (no GUI windows)
import matplotlib.pyplot as plt
import os

# ============================================
# BLOCK 1: Configuration
# ============================================

# Set the dataset path (adjust as needed)
dataset_path = "../Lung_Cancer_DataSet"  # change path if needed

categories = ["benign", "adenocarcinoma", "squamous_cell_carcinoma"]

# ============================================
# TESTING MODE - Adjust these for quick testing
# ============================================
TEST_MODE = True  # Set to False for full dataset analysis
MAX_IMAGES_PER_CATEGORY = 3  # Only load this many images per category for testing
# When TEST_MODE = False, all images will be processed

# ============================================
# BLOCK 2: Load Dataset
# ============================================

print("Loading dataset...")
print("=" * 50)

if TEST_MODE:
    print("*** TEST MODE ENABLED ***")
    print(f"   Loading max {MAX_IMAGES_PER_CATEGORY} images per category for quick testing")
    print("   Set TEST_MODE = False in the script for full analysis")
    print("=" * 50)

# Create output directory for saving figures (non-interactive mode)
output_dir = "output_figures"
os.makedirs(output_dir, exist_ok=True)
print(f"Output figures will be saved to: {output_dir}/")
print()

data = []
labels = []

for category in categories:
    folder_path = os.path.join(dataset_path, category)

    if not os.path.exists(folder_path):
        print(f"Warning: {folder_path} does not exist!")
        continue

    print(f"Loading {category} images...")
    count = 0

    img_files = os.listdir(folder_path)
    loaded = 0

    for img_name in img_files:
        # In test mode, limit images per category
        if TEST_MODE and loaded >= MAX_IMAGES_PER_CATEGORY:
            break

        img_path = os.path.join(folder_path, img_name)
        image = cv2.imread(img_path)

        if image is not None:
            data.append(image)
            labels.append(category)
            count += 1
            loaded += 1

    print(f"  - Loaded {count} images from {category}")

print("=" * 50)
print(f"Total images loaded: {len(data)}")
print()

# ============================================
# BLOCK 3: Display Sample Images
# ============================================

if len(data) > 0:
    print("Displaying sample images...")
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))

    for i in range(min(3, len(data))):
        img = cv2.cvtColor(data[i], cv2.COLOR_BGR2RGB)
        axes[i].imshow(img)
        axes[i].set_title(labels[i])
        axes[i].axis("off")

    plt.tight_layout()
    plt.savefig(f"{output_dir}/01_sample_images.png", dpi=150, bbox_inches='tight')
    plt.close()
    print()

# ============================================
# BLOCK 4: Preprocessing
# ============================================

if len(data) > 0:
    print("Applying preprocessing...")
    # Take one sample image
    image = data[0]

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian Blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Show result
    plt.figure(figsize=(8, 4))

    plt.subplot(1, 2, 1)
    plt.imshow(gray, cmap='gray')
    plt.title("Grayscale")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(blur, cmap='gray')
    plt.title("Gaussian Blur")
    plt.axis("off")

    plt.tight_layout()
    plt.savefig(f"{output_dir}/02_preprocessing.png", dpi=150, bbox_inches='tight')
    plt.close()
    print()

    # ============================================
    # BLOCK 5: Segmentation (Otsu Threshold)
    # ============================================

    print("Performing segmentation...")
    # Using Otsu Threshold (BEST)
    _, thresh = cv2.threshold(blur, 0, 255,
                             cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    plt.figure(figsize=(6, 4))
    plt.imshow(thresh, cmap='gray')
    plt.title("Segmented Image (Otsu)")
    plt.axis("off")
    plt.savefig(f"{output_dir}/03_segmentation.png", dpi=150, bbox_inches='tight')
    plt.close()
    print()

    # ============================================
    # BLOCK 6: Detect Circular Cells
    # ============================================

    print("Detecting circular cells...")
    # Copy original image for drawing
    output = image.copy()

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    print(f"Total contours found: {len(contours)}")

    cell_count = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)

        if area > 50:  # filter small noise
            perimeter = cv2.arcLength(cnt, True)

            if perimeter == 0:
                continue

            circularity = 4 * np.pi * (area / (perimeter * perimeter))

            if circularity > 0.7:  # circular shape
                cv2.drawContours(output, [cnt], -1, (0, 255, 0), 2)
                cell_count += 1

    print(f"Circular cells detected: {cell_count}")

    output_rgb = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)

    plt.figure(figsize=(6, 4))
    plt.imshow(output_rgb)
    plt.title(f"Circular Cells Detected ({cell_count} cells)")
    plt.axis("off")
    plt.savefig(f"{output_dir}/04_cells_detected.png", dpi=150, bbox_inches='tight')
    plt.close()
    print()

    # ============================================
    # BLOCK 7: Pseudo-Coloring
    # ============================================

    print("Applying pseudo-coloring...")
    color = cv2.applyColorMap(thresh, cv2.COLORMAP_JET)

    plt.figure(figsize=(6, 4))
    plt.imshow(color)
    plt.title("Pseudo Colored Image")
    plt.axis("off")
    plt.savefig(f"{output_dir}/05_pseudo_color.png", dpi=150, bbox_inches='tight')
    plt.close()
    print()

    # ============================================
    # BLOCK 8: Final Combined Output
    # ============================================

    print("Generating final combined output...")
    plt.figure(figsize=(15, 10))

    plt.subplot(2, 3, 1)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title("Original")
    plt.axis("off")

    plt.subplot(2, 3, 2)
    plt.imshow(gray, cmap='gray')
    plt.title("Grayscale")
    plt.axis("off")

    plt.subplot(2, 3, 3)
    plt.imshow(blur, cmap='gray')
    plt.title("Blur")
    plt.axis("off")

    plt.subplot(2, 3, 4)
    plt.imshow(thresh, cmap='gray')
    plt.title("Segmentation")
    plt.axis("off")

    plt.subplot(2, 3, 5)
    plt.imshow(output_rgb)
    plt.title("Detected Cells")
    plt.axis("off")

    plt.subplot(2, 3, 6)
    plt.imshow(color)
    plt.title("Pseudo Color")
    plt.axis("off")

    plt.tight_layout()
    plt.savefig(f"{output_dir}/06_final_grid.png", dpi=150, bbox_inches='tight')
    plt.close()

    print("=" * 50)
    print("Analysis Complete!")
    print("=" * 50)

    # ============================================
    # Additional Analysis: Process all images
    # ============================================

    print("\n" + "=" * 50)
    print("Processing all images in dataset...")
    print("=" * 50)

    total_cells_all_images = []
    category_cell_counts = {cat: [] for cat in categories}

    for idx, (img, label) in enumerate(zip(data, labels)):
        # Preprocess
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur_img = cv2.GaussianBlur(gray_img, (5, 5), 0)
        _, thresh_img = cv2.threshold(blur_img, 0, 255,
                                    cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Detect cells
        contours, _ = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)

        cell_count = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 50:
                perimeter = cv2.arcLength(cnt, True)
                if perimeter > 0:
                    circularity = 4 * np.pi * (area / (perimeter * perimeter))
                    if circularity > 0.7:
                        cell_count += 1

        total_cells_all_images.append(cell_count)
        category_cell_counts[label].append(cell_count)

        if (idx + 1) % 10 == 0:
            print(f"Processed {idx + 1}/{len(data)} images...")

    # Print statistics
    print("\n" + "=" * 50)
    print("STATISTICS")
    print("=" * 50)

    print(f"\nTotal images analyzed: {len(data)}")
    print(f"Total cells detected across all images: {sum(total_cells_all_images)}")
    print(f"Average cells per image: {np.mean(total_cells_all_images):.2f}")
    print(f"Maximum cells in one image: {max(total_cells_all_images)}")
    print(f"Minimum cells in one image: {min(total_cells_all_images)}")

    print("\nCell counts by category:")
    for cat in categories:
        counts = category_cell_counts[cat]
        if counts:
            print(f"  {cat}:")
            print(f"    - Images: {len(counts)}")
            print(f"    - Total cells: {sum(counts)}")
            print(f"    - Average cells/image: {np.mean(counts):.2f}")
            print(f"    - Max cells: {max(counts)}")
            print(f"    - Min cells: {min(counts)}")
        else:
            print(f"  {cat}: No images found")

    print("\n" + "=" * 50)
    print("Analysis Complete!")
    print("=" * 50)

else:
    print("No images loaded. Please check your dataset path.")
