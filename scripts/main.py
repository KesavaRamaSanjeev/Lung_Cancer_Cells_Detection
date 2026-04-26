"""
Lung Cancer Cell Detection and Pseudo-Coloring
===============================================

WHAT THIS SCRIPT DOES:
1. Load lung cancer images from dataset
2. Segment images to identify circular cancer cells
3. Apply pseudo-color transformation for visualization

Three Main Steps:
  Step 1: Segmentation (Black & White)
  Step 2: Cell Detection (Green circles on cells)
  Step 3: Pseudo-coloring (Rainbow colors on cells)

Usage:
  python main.py ../Lung_Cancer_DataSet/benign/0001.jpg
  OR
  python main.py -all
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from pathlib import Path

# Don't show plots (save instead)
plt.switch_backend('Agg')


def segment_image(image):
    """
    STEP 1: SEGMENTATION
    Converts image to Black & White to identify cells
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply blur to reduce noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Otsu's thresholding (automatic black & white conversion)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return gray, blur, thresh


def detect_cells(thresh, image):
    """
    STEP 2: CELL DETECTION
    Identifies circular cancer cells in segmented image
    """
    output = image.copy()
    
    # Find contours (outlines of cells)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    cell_count = 0
    cell_areas = []
    cell_circularities = []
    detected_cells = []
    
    # Filter cells by area and circularity
    for cnt in contours:
        area = cv2.contourArea(cnt)
        
        # Area filter: only cells larger than 50 pixels
        if area > 50:
            perimeter = cv2.arcLength(cnt, True)
            
            if perimeter > 0:
                # Circularity = how round the cell is (1.0 = perfect circle)
                circularity = 4 * np.pi * (area / (perimeter * perimeter))
                
                # Circularity filter: only cells that are round (>0.7)
                if circularity > 0.7:
                    # Draw green circle around detected cell
                    cv2.drawContours(output, [cnt], -1, (0, 255, 0), 2)
                    cell_count += 1
                    cell_areas.append(area)
                    cell_circularities.append(circularity)
                    detected_cells.append(cnt)
    
    return output, cell_count, detected_cells, cell_areas, cell_circularities, thresh


def apply_pseudo_color(image, detected_cells, thresh):
    """
    STEP 3: PSEUDO-COLORING
    Applies rainbow colors to detected cells
    """
    # Create mask with only detected cells (filled)
    cell_mask = np.zeros_like(thresh)
    cv2.drawContours(cell_mask, detected_cells, -1, 255, -1)
    
    # Apply JET colormap (blue→green→yellow→red)
    cell_colored = cv2.applyColorMap(cell_mask, cv2.COLORMAP_JET)
    cell_colored_rgb = cv2.cvtColor(cell_colored, cv2.COLOR_BGR2RGB)
    
    # Keep background black (only color the cells)
    cell_colored_rgb[cell_mask == 0] = (0, 0, 0)
    
    # Blend pseudo-colored cells with original image
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    overlay = image_rgb.copy()
    cell_pixels = cell_mask > 0
    
    if np.any(cell_pixels):
        overlay[cell_pixels] = cv2.addWeighted(
            image_rgb[cell_pixels], 0.35,
            cell_colored_rgb[cell_pixels], 0.65, 0
        )
    
    return cell_colored_rgb, overlay


def create_summary_grid(image, gray, blur, thresh, cell_output, cell_colored, overlay, cell_count):
    """
    Create a 6-panel summary showing all steps
    """
    fig = plt.figure(figsize=(15, 10))
    
    # Panel 1: Original Image
    ax1 = fig.add_subplot(2, 3, 1)
    ax1.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    ax1.set_title('Step 0: Original Image', fontsize=12, fontweight='bold')
    ax1.axis('off')
    
    # Panel 2: Grayscale
    ax2 = fig.add_subplot(2, 3, 2)
    ax2.imshow(gray, cmap='gray')
    ax2.set_title('Step 1: Grayscale', fontsize=12, fontweight='bold')
    ax2.axis('off')
    
    # Panel 3: Segmentation
    ax3 = fig.add_subplot(2, 3, 3)
    ax3.imshow(thresh, cmap='gray')
    ax3.set_title('Step 2: Segmentation (Black & White)', fontsize=12, fontweight='bold')
    ax3.axis('off')
    
    # Panel 4: Cell Detection
    ax4 = fig.add_subplot(2, 3, 4)
    ax4.imshow(cv2.cvtColor(cell_output, cv2.COLOR_BGR2RGB))
    ax4.set_title(f'Step 3: Cell Detection ({cell_count} cells)', fontsize=12, fontweight='bold')
    ax4.axis('off')
    
    # Panel 5: Pseudo-Color
    ax5 = fig.add_subplot(2, 3, 5)
    ax5.imshow(cell_colored)
    ax5.set_title('Step 4: Pseudo-Color Mask', fontsize=12, fontweight='bold')
    ax5.axis('off')
    
    # Panel 6: Overlay
    ax6 = fig.add_subplot(2, 3, 6)
    ax6.imshow(overlay)
    ax6.set_title('Step 5: Colored Cells on Original', fontsize=12, fontweight='bold')
    ax6.axis('off')
    
    fig.suptitle(f'Lung Cancer Cell Detection Pipeline', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    return fig


def analyze_single_image(image_path):
    """
    Analyze ONE image and save results
    """
    print("\n" + "="*70)
    print("LUNG CANCER CELL DETECTION & PSEUDO-COLORING")
    print("="*70)
    
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        print(f"❌ ERROR: Could not load image: {image_path}")
        return
    
    print(f"\n📷 Image: {os.path.basename(image_path)}")
    print(f"   Size: {image.shape[1]} x {image.shape[0]} pixels")
    
    # Create output folder
    output_dir = "results"
    os.makedirs(output_dir, exist_ok=True)
    
    # STEP 1: Segmentation
    print("\n[STEP 1] Segmenting image (Black & White conversion)...")
    gray, blur, thresh = segment_image(image)
    print("   ✓ Segmentation complete")
    
    # STEP 2: Cell Detection
    print("\n[STEP 2] Detecting circular cancer cells...")
    cell_output, cell_count, detected_cells, cell_areas, cell_circularities, _ = detect_cells(thresh, image)
    print(f"   ✓ Detected {cell_count} circular cells")
    
    if cell_count > 0:
        print(f"   - Average cell area: {np.mean(cell_areas):.1f} pixels²")
        print(f"   - Average circularity: {np.mean(cell_circularities):.3f}")
    
    # STEP 3: Pseudo-coloring
    print("\n[STEP 3] Applying pseudo-color transformation...")
    cell_colored, overlay = apply_pseudo_color(image, detected_cells, thresh)
    print("   ✓ Pseudo-coloring complete")
    
    # Create summary grid
    print("\n[STEP 4] Creating summary visualization...")
    fig = create_summary_grid(image, gray, blur, thresh, cell_output, cell_colored, overlay, cell_count)
    
    # Save results
    output_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(image_path))[0]}_analysis.png")
    fig.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"   ✓ Saved: {output_path}")
    
    # Save individual steps
    print("\n[STEP 5] Saving detailed results...")
    
    # Save segmentation
    fig_seg = plt.figure(figsize=(8, 6))
    plt.imshow(thresh, cmap='gray')
    plt.title('Segmentation: Black & White Image')
    plt.axis('off')
    plt.tight_layout()
    seg_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(image_path))[0]}_01_segmentation.png")
    fig_seg.savefig(seg_path, dpi=150, bbox_inches='tight')
    plt.close(fig_seg)
    print(f"   ✓ Saved: {seg_path}")
    
    # Save cell detection
    fig_cells = plt.figure(figsize=(8, 6))
    plt.imshow(cv2.cvtColor(cell_output, cv2.COLOR_BGR2RGB))
    plt.title(f'Cell Detection: {cell_count} Cells Found')
    plt.axis('off')
    plt.tight_layout()
    cells_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(image_path))[0]}_02_detected_cells.png")
    fig_cells.savefig(cells_path, dpi=150, bbox_inches='tight')
    plt.close(fig_cells)
    print(f"   ✓ Saved: {cells_path}")
    
    # Save pseudo-color
    fig_pseudo = plt.figure(figsize=(8, 6))
    plt.imshow(overlay)
    plt.title('Pseudo-Color Transformation')
    plt.axis('off')
    plt.tight_layout()
    pseudo_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(image_path))[0]}_03_pseudo_color.png")
    fig_pseudo.savefig(pseudo_path, dpi=150, bbox_inches='tight')
    plt.close(fig_pseudo)
    print(f"   ✓ Saved: {pseudo_path}")
    
    # Print results
    print("\n" + "="*70)
    print("RESULTS SUMMARY")
    print("="*70)
    print(f"Total cells detected: {cell_count}")
    
    if cell_count == 0:
        print("⚠️  No cells detected - image may not be lung tissue")
    elif cell_count < 5:
        print("ℹ️  Low cell count - possibly benign tissue")
    else:
        print("⚠️  High cell count - possibly cancerous tissue")
    
    print(f"\nAll results saved to: {output_dir}/")
    print("="*70 + "\n")


def analyze_all_images(dataset_path):
    """
    Analyze ALL images in dataset
    """
    categories = ["benign", "adenocarcinoma", "squamous_cell_carcinoma"]
    
    print("\n" + "="*70)
    print("ANALYZING ALL IMAGES IN DATASET")
    print("="*70)
    
    for category in categories:
        cat_path = os.path.join(dataset_path, category)
        
        if not os.path.exists(cat_path):
            print(f"\n❌ {category}: Folder not found")
            continue
        
        image_files = [f for f in os.listdir(cat_path) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
        
        print(f"\n📁 {category}: {len(image_files)} images")
        
        # Process first 3 images as example
        for i, img_file in enumerate(image_files[:3]):
            img_path = os.path.join(cat_path, img_file)
            print(f"  [{i+1}/3] Processing: {img_file}")
            analyze_single_image(img_path)


def main():
    print("\n" + "="*70)
    print("LUNG CANCER CELL DETECTION & PSEUDO-COLORING")
    print("="*70)
    
    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python main.py <image_path>")
        print("  python main.py -all")
        print("\nExamples:")
        print("  python main.py ../Lung_Cancer_DataSet/benign/0001.jpg")
        print("  python main.py -all")
        print("\nWhat this does:")
        print("  1. SEGMENTATION: Converts to black & white")
        print("  2. CELL DETECTION: Identifies circular cells")
        print("  3. PSEUDO-COLORING: Applies rainbow colors to cells")
        sys.exit(1)
    
    if sys.argv[1] == "-all":
        # Analyze all images
        dataset_path = "../Lung_Cancer_DataSet"
        if not os.path.exists(dataset_path):
            print(f"❌ Dataset not found at: {dataset_path}")
            sys.exit(1)
        analyze_all_images(dataset_path)
    else:
        # Analyze single image
        image_path = sys.argv[1]
        if not os.path.exists(image_path):
            print(f"❌ Image not found: {image_path}")
            sys.exit(1)
        analyze_single_image(image_path)


if __name__ == "__main__":
    main()
