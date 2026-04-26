"""
Interactive Lung Cancer Image Analysis
=======================================
Upload YOUR OWN image and analyze it step by step.

Features:
- Upload any lung histopathology image
- Choose between file dialog or manual path entry
- Process with same pipeline (preprocess, segment, detect cells)
- Save all outputs
- Get statistics for that single image
"""

import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import os
import sys

def upload_image_gui():
    """Open file dialog to select image (requires tkinter)."""
    try:
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()  # Hide the main window

        file_types = [
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif"),
            ("All files", "*.*")
        ]

        file_path = filedialog.askopenfilename(
            title="Select Lung Histopathology Image",
            filetypes=file_types
        )

        root.destroy()

        if file_path:
            return file_path
        else:
            return None

    except ImportError:
        print("❌ tkinter not available. Use manual path entry instead.")
        return None

def upload_image_manual():
    """Ask user to type the image path."""
    print("\n" + "=" * 60)
    print("UPLOAD YOUR IMAGE")
    print("=" * 60)
    print("\nPlease enter the full path to your image file.")
    print("Example: C:\\Users\\YourName\\Downloads\\sample.jpg")
    print("Or: ./my_image.png")
    print("\nPress Enter to cancel.")

    file_path = input("\nImage path: ").strip()

    if file_path == "":
        return None

    # Expand relative paths
    file_path = os.path.expanduser(file_path)
    file_path = os.path.abspath(file_path)

    return file_path

def load_image(file_path):
    """Load and validate the uploaded image."""
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return None

    # Check file extension
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif')
    if not file_path.lower().endswith(valid_extensions):
        print(f"⚠️  Warning: Unexpected file extension. Expected image file.")

    # Load image
    image = cv2.imread(file_path)

    if image is None:
        print(f"❌ Failed to load image. File may be corrupted or not an image.")
        return None

    print(f"✅ Image loaded successfully!")
    print(f"   Path: {file_path}")
    print(f"   Size: {image.shape[1]} x {image.shape[0]} pixels")
    print(f"   Channels: {image.shape[2] if len(image.shape) == 3 else 1}")

    return image

def analyze_image(image, file_path, output_dir="interactive_output"):
    """Run full analysis pipeline on the uploaded image."""
    os.makedirs(output_dir, exist_ok=True)

    print("\n" + "=" * 60)
    print("STARTING IMAGE ANALYSIS")
    print("=" * 60)

    # ========================================
    # BLOCK 1: Preprocessing
    # ========================================
    print("\n[1/6] Preprocessing...")
    print("-" * 60)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian Blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Save preprocessing figure
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].imshow(gray, cmap='gray')
    axes[0].set_title("Grayscale")
    axes[0].axis("off")
    axes[1].imshow(blur, cmap='gray')
    axes[1].set_title("Gaussian Blur (5x5)")
    axes[1].axis("off")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/01_preprocessing.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("   ✓ Grayscale conversion")
    print("   ✓ Gaussian blur applied")
    print(f"   Saved: {output_dir}/01_preprocessing.png")

    # ========================================
    # BLOCK 2: Segmentation (Otsu)
    # ========================================
    print("\n[2/6] Segmentation (Otsu Threshold)...")
    print("-" * 60)

    _, thresh = cv2.threshold(blur, 0, 255,
                             cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    otsu_threshold = _
    print(f"   Otsu threshold value: {otsu_threshold}")

    # Save segmentation figure
    plt.figure(figsize=(6, 4))
    plt.imshow(thresh, cmap='gray')
    plt.title(f"Segmented Image (Otsu Threshold = {otsu_threshold})")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/02_segmentation.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   ✓ Binary segmentation applied")
    print(f"   Saved: {output_dir}/02_segmentation.png")

    # ========================================
    # BLOCK 3: Cell Detection
    # ========================================
    print("\n[3/6] Detecting Circular Cells...")
    print("-" * 60)

    output = image.copy()

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)

    print(f"   Total contours found: {len(contours)}")

    # Filter contours by area and circularity
    cell_count = 0
    cell_areas = []
    cell_circularities = []

    for cnt in contours:
        area = cv2.contourArea(cnt)

        if area > 50:  # Minimum area filter
            perimeter = cv2.arcLength(cnt, True)

            if perimeter > 0:
                circularity = 4 * np.pi * (area / (perimeter * perimeter))

                if circularity > 0.7:  # Circularity filter
                    cv2.drawContours(output, [cnt], -1, (0, 255, 0), 2)
                    cell_count += 1
                    cell_areas.append(area)
                    cell_circularities.append(circularity)

    print(f"   Filtered (area > 50): {len([a for a in cell_areas if a > 0])}")
    print(f"   Circular cells detected: {cell_count}")

    if cell_count > 0:
        print(f"   Average cell area: {np.mean(cell_areas):.2f} pixels")
        print(f"   Average circularity: {np.mean(cell_circularities):.3f}")

    # Save cell detection figure
    output_rgb = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
    plt.figure(figsize=(8, 6))
    plt.imshow(output_rgb)
    plt.title(f"Detected Circular Cells: {cell_count}")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/03_cells_detected.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   ✓ Green contours drawn around {cell_count} cells")
    print(f"   Saved: {output_dir}/03_cells_detected.png")

    # ========================================
    # BLOCK 4: Pseudo-Coloring
    # ========================================
    print("\n[4/6] Creating Pseudo-Color Visualization...")
    print("-" * 60)

    color = cv2.applyColorMap(thresh, cv2.COLORMAP_JET)

    plt.figure(figsize=(6, 4))
    plt.imshow(color)
    plt.title("Pseudo-Colored Segmentation (JET)")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/04_pseudo_color.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   ✓ JET colormap applied")
    print(f"   Saved: {output_dir}/04_pseudo_color.png")

    # ========================================
    # BLOCK 5: Overlay View
    # ========================================
    print("\n[5/6] Creating Overlay Visualization...")
    print("-" * 60)

    # Create overlay: blend original with cell contours
    overlay = image.copy()
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 50:
            perimeter = cv2.arcLength(cnt, True)
            if perimeter > 0:
                circularity = 4 * np.pi * (area / (perimeter * perimeter))
                if circularity > 0.7:
                    cv2.drawContours(overlay, [cnt], -1, (0, 255, 0), 2)

    overlay_rgb = cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB)

    plt.figure(figsize=(6, 4))
    plt.imshow(overlay_rgb)
    plt.title("Overlay: Cells Highlighted")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/05_overlay.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   ✓ Overlay created with detected cells")
    print(f"   Saved: {output_dir}/05_overlay.png")

    # ========================================
    # BLOCK 6: Final Grid
    # ========================================
    print("\n[6/6] Generating Final Summary Grid...")
    print("-" * 60)

    plt.figure(figsize=(15, 10))

    plt.subplot(2, 3, 1)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title("1. Original")
    plt.axis("off")

    plt.subplot(2, 3, 2)
    plt.imshow(gray, cmap='gray')
    plt.title("2. Grayscale")
    plt.axis("off")

    plt.subplot(2, 3, 3)
    plt.imshow(blur, cmap='gray')
    plt.title("3. Blur")
    plt.axis("off")

    plt.subplot(2, 3, 4)
    plt.imshow(thresh, cmap='gray')
    plt.title("4. Segmentation")
    plt.axis("off")

    plt.subplot(2, 3, 5)
    plt.imshow(output_rgb)
    plt.title(f"5. Cells: {cell_count}")
    plt.axis("off")

    plt.subplot(2, 3, 6)
    plt.imshow(color)
    plt.title("6. Pseudo-Color")
    plt.axis("off")

    plt.suptitle("Interactive Lung Cancer Analysis - Complete Pipeline", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/06_final_grid.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   ✓ Final grid with all 6 steps")
    print(f"   Saved: {output_dir}/06_final_grid.png")

    # ========================================
    # Statistics Summary
    # ========================================
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE - RESULTS SUMMARY")
    print("=" * 60)

    print(f"\nImage analyzed: {os.path.basename(file_path)}")
    print(f"Image dimensions: {image.shape[1]} x {image.shape[0]} pixels")

    print("\n--- Detection Results ---")
    print(f"Total contours found:   {len(contours)}")
    print(f"Cells detected:         {cell_count}")

    if cell_count > 0:
        print(f"Average cell area:      {np.mean(cell_areas):.2f} pixels²")
        print(f"Average circularity:    {np.mean(cell_circularities):.3f}")
        print(f"Cell density:           {cell_count / (image.shape[0] * image.shape[1]) * 10000:.2f} cells / 10k pixels")

    print("\n--- Interpretation ---")
    if cell_count == 0:
        print("⚠️  No cells were detected.")
        print("   Possible reasons:")
        print("   - Image is not a histopathology slide")
        print("   - Cells are too small (area < 50 pixels)")
        print("   - Cells are not circular enough")
        print("   - Try adjusting parameters in the code")
    elif cell_count < 10:
        print("ℹ️  Low cell count detected.")
        print("   This could indicate:")
        print("   - Benign tissue (fewer cells)")
        print("   - Poor image quality")
        print("   - Low magnification")
    else:
        print("⚠️  Multiple cells detected.")
        print("   Higher cell count may indicate:")
        print("   - Malignant tissue (adenocarcinoma)")
        print("   - Inflammatory tissue")
        print("   - Normal tissue with many cells")

    print("\n--- Important Disclaimer ---")
    print("   ⚠️  This is an AUTOMATED ANALYSIS tool for educational purposes.")
    print("   ⚠️  Results are NOT a medical diagnosis.")
    print("   ⚠️  Consult a qualified pathologist for actual diagnosis.")

    print("\n" + "=" * 60)
    print(f"All output images saved to: {output_dir}/")
    print("=" * 60)

    return {
        'cell_count': cell_count,
        'total_contours': len(contours),
        'avg_area': np.mean(cell_areas) if cell_areas else 0,
        'avg_circularity': np.mean(cell_circularities) if cell_circularities else 0
    }

def main():
    """Main function - interactive upload and analysis."""
    print("=" * 60)
    print("INTERACTIVE LUNG CANCER IMAGE ANALYSIS")
    print("=" * 60)
    print("\nThis tool analyzes lung histopathology images.")
    print("It detects circular cell nuclei using computer vision.")
    print("\nPlease choose how to upload your image:")

    # ========================================
    # Upload Method Selection
    # ========================================
    while True:
        print("\nOptions:")
        print("  1. Use file browser (graphical)")
        print("  2. Type image path manually")
        print("  3. Exit")

        choice = input("\nEnter choice (1-3): ").strip()

        if choice == "1":
            file_path = upload_image_gui()
            if file_path:
                break
            else:
                print("No file selected. Try again or choose option 2.")
        elif choice == "2":
            file_path = upload_image_manual()
            if file_path:
                break
            else:
                print("Invalid path or cancelled. Try again.")
        elif choice == "3":
            print("Exiting program.")
            return
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    # ========================================
    # Load and Analyze
    # ========================================
    print("\n" + "=" * 60)
    print("LOADING IMAGE")
    print("=" * 60)

    image = load_image(file_path)

    if image is None:
        print("\n❌ Failed to load image. Exiting.")
        return

    # Analyse the image
    results = analyze_image(image, file_path)

    # ========================================
    # Optional: Compare with dataset statistics
    # ========================================
    print("\n" + "=" * 60)
    print("Would you like to compare with typical values?")
    print("=" * 60)
    print("\nTypical cell counts (from training dataset):")
    print("  Benign:              ~2 cells/image")
    print("  Adenocarcinoma:      ~4 cells/image")
    print("  Squamous cell:       ~0.3 cells/image")

    if results['cell_count'] > 0:
        print(f"\nYour result: {results['cell_count']} cells detected")

        if results['cell_count'] >= 4:
            print("\n→ Your image shows a cell count similar to ADENOCARCINOMA")
            print("  (higher cellular density, potentially malignant)")
        elif results['cell_count'] >= 2:
            print("\n→ Your image shows a cell count similar to BENIGN")
            print("  (moderate cellularity)")
        else:
            print("\n→ Your image shows very few cells (similar to squamous cell)")
            print("  This is unusual and may indicate:")
            print("  - Non-lung tissue")
            print("  - Very high magnification where only few nuclei fit in frame")
            print("  - Poor staining or image quality")

    print("\n" + "=" * 60)
    print("PROGRAM COMPLETE")
    print("=" * 60)
    print("\nCheck the 'interactive_output/' folder for all images.")
    print("You can run this program again with another image!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting...")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please check that your image file is valid and try again.")
