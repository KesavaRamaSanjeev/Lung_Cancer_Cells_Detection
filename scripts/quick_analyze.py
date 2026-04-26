"""
Quick Lung Image Analyzer - Single Image
=========================================
Usage: python quick_analyze.py <image_path>

Example:
  python quick_analyze.py test_image.jpg
  python quick_analyze.py "C:\\path\\to\\image.png"

This analyzes ONE image and saves outputs to 'quick_output/' folder.
"""

import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python quick_analyze.py <image_path>")
        print("\nExample:")
        print("  python quick_analyze.py test_image.jpg")
        print("  python quick_analyze.py ../Lung_Cancer_DataSet/benign/0001.jpg")
        sys.exit(1)

    image_path = sys.argv[1]

    print("=" * 60)
    print("QUICK LUNG IMAGE ANALYSIS")
    print("=" * 60)
    print(f"\nAnalyzing: {image_path}")

    # Load image
    image = cv2.imread(image_path)

    if image is None:
        print(f"❌ ERROR: Could not load image from: {image_path}")
        print("   Check if the file exists and is a valid image.")
        sys.exit(1)

    print(f"Image loaded: {image.shape[1]} x {image.shape[0]} pixels")

    # Create output folder
    output_dir = "quick_output"
    os.makedirs(output_dir, exist_ok=True)

    # ========================================
    # Step 1: Preprocess
    # ========================================
    print("\n[1] Preprocessing...")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].imshow(gray, cmap='gray')
    axes[0].set_title("Grayscale")
    axes[0].axis("off")
    axes[1].imshow(blur, cmap='gray')
    axes[1].set_title("Gaussian Blur")
    axes[1].axis("off")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/1_preprocessing.png", dpi=150, bbox_inches='tight')
    plt.close()

    # ========================================
    # Step 2: Segmentation
    # ========================================
    print("[2] Segmentation (Otsu)...")
    _, thresh = cv2.threshold(blur, 0, 255,
                             cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    plt.figure(figsize=(6, 4))
    plt.imshow(thresh, cmap='gray')
    plt.title(f"Segmentation (threshold={_})")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/2_segmentation.png", dpi=150, bbox_inches='tight')
    plt.close()

    # ========================================
    # Step 3: Cell Detection
    # ========================================
    print("[3] Detecting cells...")
    output = image.copy()
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)

    # Store detected cell contours
    detected_cells = []
    cell_count = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 50:
            perimeter = cv2.arcLength(cnt, True)
            if perimeter > 0:
                circularity = 4 * np.pi * (area / (perimeter * perimeter))
                if circularity > 0.7:
                    cv2.drawContours(output, [cnt], -1, (0, 255, 0), 2)
                    detected_cells.append(cnt)
                    cell_count += 1

    output_rgb = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
    plt.figure(figsize=(6, 4))
    plt.imshow(output_rgb)
    plt.title(f"Detected Cells: {cell_count}")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/3_cells.png", dpi=150, bbox_inches='tight')
    plt.close()

    print(f"   Found {cell_count} circular cells")

    # ========================================
    # Step 4: Pseudo-color for Cancer Cells
    # ========================================
    print("[4] Pseudo-coloring cancer cells...")
    # Create a mask with only detected cancer cells
    cell_mask = np.zeros_like(thresh)
    cv2.drawContours(cell_mask, detected_cells, -1, 255, -1)  # -1 = filled
    
    # Apply pseudo-color to the detected cell mask and keep background black
    cell_colored_bgr = cv2.applyColorMap(cell_mask, cv2.COLORMAP_JET)
    cell_colored_rgb = cv2.cvtColor(cell_colored_bgr, cv2.COLOR_BGR2RGB)
    cell_colored_rgb[cell_mask == 0] = (0, 0, 0)

    # Create an RGB overlay where only detected cells are colorized
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    colored_overlay = image_rgb.copy()
    cell_pixels = cell_mask > 0
    if np.any(cell_pixels):
        colored_overlay[cell_pixels] = cv2.addWeighted(
            image_rgb[cell_pixels], 0.35, cell_colored_rgb[cell_pixels], 0.65, 0
        )
    
    # Display pseudo-colored cancer cells
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    axes[0].imshow(cell_colored_rgb)
    axes[0].set_title(f"Pseudo-Color Mask ({cell_count} cells)")
    axes[0].axis("off")
    
    axes[1].imshow(colored_overlay)
    axes[1].set_title("Colored Cells on Original Image")
    axes[1].axis("off")
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/4_pseudocolor.png", dpi=150, bbox_inches='tight')
    plt.close()

    # ========================================
    # Step 5: Comparison Grid
    # ========================================
    print("[5] Creating summary grid...")
    plt.figure(figsize=(14, 10))

    plt.subplot(2, 3, 1)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title("Original Image")
    plt.axis("off")

    plt.subplot(2, 3, 2)
    plt.imshow(blur, cmap='gray')
    plt.title("Blur")
    plt.axis("off")

    plt.subplot(2, 3, 3)
    plt.imshow(thresh, cmap='gray')
    plt.title("Segmented (Otsu)")
    plt.axis("off")

    plt.subplot(2, 3, 4)
    plt.imshow(output_rgb)
    plt.title(f"Detected Cells: {cell_count}")
    plt.axis("off")

    plt.subplot(2, 3, 5)
    plt.imshow(cell_colored_rgb)
    plt.title("Pseudo-Color Mask")
    plt.axis("off")

    plt.subplot(2, 3, 6)
    plt.imshow(colored_overlay)
    plt.title(f"Colored Cells (Final)")
    plt.axis("off")

    plt.suptitle(f"Analysis: {os.path.basename(image_path)}", fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/5_summary.png", dpi=150, bbox_inches='tight')
    plt.close()

    # ========================================
    # Results
    # ========================================
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"Image:     {os.path.basename(image_path)}")
    print(f"Contours:  {len(contours)}")
    print(f"Cells:     {cell_count}")
    print(f"\nOutputs saved to: {output_dir}/")
    print("=" * 60)

    if cell_count >= 4:
        print("\nInterpretation: HIGH cell count (similar to adenocarcinoma)")
    elif cell_count >= 2:
        print("\nInterpretation: MODERATE cell count (similar to benign)")
    else:
        print("\nInterpretation: LOW cell count")

    print("\nThis is for educational purposes only, not medical diagnosis!")

if __name__ == "__main__":
    main()
