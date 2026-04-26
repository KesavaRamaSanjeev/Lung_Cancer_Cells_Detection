# 🫁 Lung Cancer Cell Detection & Pseudo-Coloring

A simple Digital Image Processing project that identifies circular cancer cells in lung tissue images using segmentation and applies pseudo-color transformation for visualization.

---

## 📋 What Does This Project Do?

This project performs **3 main tasks**:

### **Task 1: SEGMENTATION (Black & White)**
- Converts the lung tissue image to pure black & white
- Separates cells (white) from background (black)
- Uses Otsu's automatic thresholding technique

### **Task 2: CELL DETECTION (Green Circles)**
- Identifies circular shapes in the segmented image
- Filters cells by:
  - **Size**: Must be larger than 50 pixels
  - **Roundness**: Must have circularity > 0.7 (close to circular)
- Draws green circles around detected cells

### **Task 3: PSEUDO-COLORING (Rainbow Colors)**
- Applies JET colormap (rainbow colors: blue→green→yellow→red)
- Colors the detected cancer cells
- Makes visualization clearer and more beautiful

---

## 🗂️ Project Structure

```
DIP_Project/
├── scripts/
│   └── main.py                    ← THE ONLY PYTHON FILE (does everything!)
├── Lung_Cancer_DataSet/           ← Your dataset (3 categories)
│   ├── benign/                    ← Non-cancerous images
│   ├── adenocarcinoma/            ← Cancer cells (type 1)
│   └── squamous_cell_carcinoma/   ← Cancer cells (type 2)
├── requirements.txt               ← Dependencies
└── README.md                      ← This file
```

---

## 📦 Installation

### Step 1: Install Python Packages
```bash
pip install -r requirements.txt
```

This installs:
- **opencv-python** (cv2) - Image processing
- **numpy** - Mathematical operations
- **matplotlib** - Image visualization

---

## 🚀 How to Use

Navigate to the scripts folder:
```bash
cd scripts
```

### Option 1: Analyze ONE Image

```bash
python main.py ../Lung_Cancer_DataSet/benign/0001.jpg
```

**Output:** 
- 4 PNG files in `results/` folder showing all steps

### Option 2: Analyze ALL Images (First 3 per Category)

```bash
python main.py -all
```

**Output:**
- Multiple result folders with analysis for each category

---

## 📊 Example Output

When you run the script, you get **4 output images**:

### **Image 1: Segmentation**
```
Original tissue → Black & White image
Shows: Cells (white) vs Background (black)
```

### **Image 2: Cell Detection**  
```
Original tissue with GREEN CIRCLES around detected cells
Shows: How many cancer cells were found
```

### **Image 3: Pseudo-Color**
```
Detected cells colored with rainbow (JET colormap)
Shows: Beautiful visualization of cells
```

### **Image 4: Complete Summary**
```
6-panel grid showing:
1. Original image
2. Grayscale
3. Segmentation
4. Cell detection
5. Pseudo-color
6. Overlay
```

---

## 🎯 Understanding the Process

### **Segmentation (Task 1)**
```
Color Image → Grayscale → Blur → Otsu Threshold → Black & White
                                         ↑
                                   Automatic
                                   conversion
```

### **Cell Detection (Task 2)**
```
Black & White Image → Find Contours → Filter by Area → Filter by Circularity → Green Circles
```

**Circularity Formula:**
```
Circularity = 4π × (Area / Perimeter²)
- Perfect circle: 1.0
- Our threshold: > 0.7 (roughly circular)
```

### **Pseudo-Coloring (Task 3)**
```
Detected Cells → Apply JET Colormap → Rainbow Colors
              Blue → Green → Yellow → Red
```

---

## 📈 Results Interpretation

| Cell Count | Likely Diagnosis |
|-----------|-----------------|
| 0-2 | Benign (non-cancerous) |
| 3-5 | Benign (moderate) |
| 6+ | Adenocarcinoma (cancerous) |

**⚠️ Important:** This is an **educational tool ONLY**. Real diagnosis requires expert pathologist review!

---

## 💻 System Requirements

- **Python**: 3.8 or higher
- **OS**: Windows, Mac, or Linux
- **RAM**: 4GB minimum
- **Disk**: 500MB free space

---

## 📝 File Descriptions

### **main.py** (The Only Python File)

Contains these functions:

1. **`segment_image(image)`**
   - Task 1: Converts to grayscale, blurs, and segments using Otsu

2. **`detect_cells(thresh, image)`**
   - Task 2: Finds contours and filters by area & circularity

3. **`apply_pseudo_color(image, detected_cells, thresh)`**
   - Task 3: Applies JET colormap to detected cells

4. **`analyze_single_image(image_path)`**
   - Main function: Runs all 3 tasks on ONE image

5. **`analyze_all_images(dataset_path)`**
   - Runs analysis on all images in dataset

---

## 🔧 Customization

You can modify these parameters in `main.py`:

```python
# Minimum cell size (pixels)
if area > 50:  # Change this value

# Circularity threshold (0.0 to 1.0)
if circularity > 0.7:  # Change this value

# Blur kernel size (must be odd)
blur = cv2.GaussianBlur(gray, (5, 5), 0)  # Change to (7,7) or (9,9)
```

---

## 📚 Key Concepts

### **Otsu's Thresholding**
- Automatically finds the best threshold to separate foreground & background
- Works best with images that have 2 distinct intensity levels
- Perfect for histopathology images (dark cells + light background)

### **Contour Detection**
- Finds outlines/edges of objects in an image
- Uses `cv2.findContours()` with `RETR_EXTERNAL` (only outer contours)

### **Circularity**
- Measures how circular a shape is
- Formula: `4π × (Area / Perimeter²)`
- Used to filter real cells (circular) from noise (irregular)

### **Pseudo-Coloring**
- Maps grayscale intensity to colors
- JET colormap: Blue (low) → Green → Yellow → Red (high)
- Makes subtle differences more visible to human eye

---

## 🐛 Troubleshooting

### "Image not found" Error
```bash
# Wrong path
python main.py Lung_Cancer_DataSet/benign/0001.jpg

# Correct path (from scripts folder)
python main.py ../Lung_Cancer_DataSet/benign/0001.jpg
```

### "Module not found" Error
```bash
# Install dependencies
pip install -r ../requirements.txt
```

### No cells detected
- Image might not be lung tissue
- Cells might be too small (increase blur or decrease area threshold)
- Cells might be irregular (decrease circularity threshold)

---

## 📖 Learning Resources

**Read the code comments in main.py** - They explain everything step by step!

---

## ✅ Summary

This project teaches you:
- ✓ Image Segmentation (Otsu's thresholding)
- ✓ Contour Detection & Analysis
- ✓ Shape Filtering (Area & Circularity)
- ✓ Pseudo-color Transformation (JET colormap)
- ✓ OpenCV & Image Processing in Python

---

## 📞 Questions?

Read the comments in **main.py** - everything is clearly explained!

---

**Happy Learning!** 🎉
