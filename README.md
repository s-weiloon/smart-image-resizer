# Batch Image Resizer

A straightforward, internal desktop utility for batch processing and resizing images.

<div align="center">
<img src="icon.ico" alt="Tool Icon" width="100"/>
</div>

---

## What It Does

This tool allows you to select a folder of images and automatically resize them in bulk. It standardizes image dimensions efficiently for internal workflows by automatically detecting image orientation and applying appropriate dimension ceilings or oversize limits.

---

## How It Works

The application scans the selected directory for supported image formats (`PNG`, `JPG`, `JPEG`, `BMP`, `WEBP`, `TIFF`) and applies the following conditional logic to each file:

- **Oversize Protection:** If an image's width exceeds a user-defined limit, it is forcefully scaled down to a specified maximum size to prevent unusually large files.
- **Orientation Detection:** The tool automatically detects whether the image is **Landscape** (`width > height`), **Portrait** (`height > width`), or triggers the **Oversize** (Playmat) rule based on its width.
- **Smart Rescaling:** Once categorized, each image is assigned its corresponding target dimensions and resized while strictly maintaining the original aspect ratio *(utilizing Lanczos resampling)*.
- **File Output:** By default, it generates safe copies appended with `-resized` in the same directory. If the **Overwrite** toggle is enabled, it replaces the original source files.

### Resize Categories

| Category | Trigger Condition | Default Output |
|---|---|---|
| **Oversize / Playmat** | Width exceeds the oversize limit (width) | e.g. 2500 × 1406 |
| **Landscape** | Width > Height | e.g. 1920 × 1080 |
| **Portrait** | Height ≥ Width | e.g. 1080 × 1920 |
---

## How To Use

1. **Select Folder** — Click **"Select Image Folder"** to choose the target directory containing your images.
2. **Configure Dimensions** — Set the maximum output dimensions for **Landscape**, **Portrait**, and **Oversize** limits *(sensible defaults are pre-populated)*.
3. **Overwrite Setting** — Toggle **"Overwrite original images"** only if you want to permanently replace the source files. Keeping this off is recommended to prevent data loss.
4. **Execute** — Click **"Start Resizing"**. You can track the progress and see the specific resizing logic applied to each file in the **Job History** panel at the bottom of the window.

---

## Installation & Setup

### 1. Clone the repository
```bash
git clone [<repository_url>](https://github.com/s-weiloon/smart-image-resizer.git)
cd <repository_folder>
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

Install the required packages using the provided `requirements.txt` file.
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
python image_resizer.py
```
