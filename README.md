# PixelFlow Studio

A modern, light-weight, open-source desktop application for batch image resizing built with Python and CustomTkinter.

<div align="center">
  <img src="icon.ico" alt="PixelFlow Studio Logo" width="150"/>
</div>

---

## ✨ Features
* **Batch Processing**: Resize entire directories of images instantly.
* **Smart Aspect Ratio Handling**: Automatically detects landscape vs. portrait images and applies the appropriate dimension ceilings.
* **Oversize Protection**: Built-in logic to safely downscale excessively large images.
* **Job History**: Visual representation of processed images with original vs. new thumbnails and success tracking. 

## 🚀 Installation & Setup 

### 1. Clone the repository
```cmd
git clone https://github.com/yourusername/image-resizer-dec-25.git
cd image-resizer-dec-25
```

### 2. Create a Virtual Environment (Recommended)
```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install Requirements
Install all necessary packages via the included `requirements.txt`:
```cmd
pip install -r requirements.txt
```

### 4. Run the Application
```cmd
python image_resizer.py
```

## 🛠️ Technology Stack
- **[Python](https://www.python.org/)** - Core programming language
- **[CustomTkinter](https://customtkinter.tomschimansky.com/)** - Modern GUI framework
- **[Pillow (PIL)](https://python-pillow.org/)** - Powerful image processing library
- **[pywinstyles](https://github.com/Akascape/pywinstyles)** - Adds Windows 11 Mica glassmorphism UI styles

## ⚠️ Notes

- Using the `Overwrite original images` option is destructive. It is recommended to keep it disabled to generate safe `-resized` copies instead.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.
