# RightClickResizer

A simple tool that adds a "Resize Image" option to the Windows context menu for image files.

## Features

- Right-click on any image file to resize it
- Supports JPG, JPEG, PNG, BMP, WebP, and GIF files
- Creates a resized copy with `_resized` suffix
- Configurable max width, height, and quality

## Installation

1. Download the latest release from [GitHub Releases](https://github.com/ardabilgen/RightClickResizer/releases).
2. Run `RightClickResizer.exe` **as Administrator**.
3. Click "Install Context Menu".

Or build from source:
1. Run `build.bat` to create the `.exe` file.
2. Run `dist/RightClickResizer.exe` as Administrator.
3. Click "Install Context Menu".

## Usage

1. Right-click on any image file (JPG, PNG, etc.).
2. Click "Resize Image".
3. A resized copy with `_resized` suffix will be created in the same directory.

## Settings

Run the program directly (without right-clicking on a file) to adjust:
- Max width
- Max height  
- Quality (1-100)

## Uninstall

Run the program as Administrator and click "Uninstall".

---
*Made with Antigravity*