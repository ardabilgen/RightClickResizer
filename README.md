# ⚡ RightClickResizer

**Windows context menu tool for resizing images and converting videos to MP4**

A lightweight Windows application that adds convenient "Resize" and "Convert" options to your right-click context menu. Process images and videos instantly without opening any software.

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)

---

## 🚀 Features

### 🖼️ Image Resizing
- Right-click on any image file to resize instantly
- Supports: **JPG, JPEG, PNG, BMP, WebP, GIF**
- Configurable max width, height, and quality
- Creates a `_resized` copy (original is preserved)

### 🎬 Video Conversion
- Right-click on any video file to convert to MP4
- Supports: **MP4, AVI, MOV, MKV, WMV, FLV, WebM, M4V, MPEG, MPG**
- H.264 encoding with configurable quality (CRF 18-28)
- Automatic file size reduction while maintaining quality
- Creates a `_converted.mp4` file (original is preserved)

### 🔧 Built-in ffmpeg
- ffmpeg is **embedded** inside the executable — no separate installation needed
- Works out of the box after installation

---

## 📦 Installation

### Option 1: Download Release (Recommended)

1. Download the latest `RightClickResizer.exe` from [GitHub Releases](https://github.com/ardabilgen/RightClickResizer/releases)
2. Run `RightClickResizer.exe` **as Administrator**
3. Click **"Install Context Menu"**
4. Done! Right-click on any image or video file

### Option 2: Build from Source

```bash
# Clone the repository
git clone https://github.com/ardabilgen/RightClickResizer.git
cd RightClickResizer

# Run the build script (requires Python 3.8+)
build.bat
```

The executable will be created in `dist/RightClickResizer.exe`.

---

## 🎯 Usage

### Images
1. Right-click on any image file (JPG, PNG, BMP, etc.)
2. Select **"Resize Image"**
3. A resized copy with `_resized` suffix is created in the same folder

### Videos
1. Right-click on any video file (MP4, AVI, MOV, MKV, etc.)
2. Select **"Convert to MP4"**
3. A converted MP4 file with `_converted.mp4` suffix is created

### Settings
Run `RightClickResizer.exe` directly (without right-clicking) to open the settings window:

| Setting | Description | Default |
|---------|-------------|---------|
| **Max Width** | Maximum image width | 1920 |
| **Max Height** | Maximum image height | 1080 |
| **Quality** | Image quality (1-100) | 85 |
| **CRF** | Video quality (18-28, lower=better) | 23 |
| **Preset** | Encoding speed (slower=smaller) | medium |
| **Video Max Width** | Max video width | 1920 |
| **Video Max Height** | Max video height | 1080 |

---

## 🧹 Uninstall

1. Run `RightClickResizer.exe` as Administrator
2. Click **"Uninstall"**
3. Context menu entries are removed

---

## 🏗️ Architecture

```
RightClickResizer/
├── src/
│   ├── main.py           # Entry point + GUI
│   ├── resizer.py         # Image resizing (Pillow)
│   ├── video_converter.py # Video conversion (ffmpeg)
│   ├── context_menu.py    # Windows registry integration
│   └── config.py          # Settings management
├── tests/                 # Unit tests
├── build.bat              # Build script
├── requirements.txt       # Python dependencies
└── README.md
```

---

## 📝 Technical Details

### Image Resizing
- Uses **Pillow (PIL)** for fast, high-quality resizing
- BICUBIC resampling for smooth results
- Aspect ratio is always preserved

### Video Conversion
- Uses **ffmpeg 8.0** with H.264 (libx264) encoding
- CRF (Constant Rate Factor) mode for quality-based encoding
- Audio stream is copied without re-encoding (fast, lossless)
- Web-optimized output (faststart flag)

---

## 📄 License

MIT License — see [LICENSE](LICENSE) file.

---

*Made with ❤️ and Antigravity*
