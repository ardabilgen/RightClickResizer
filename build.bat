@echo off
echo ========================================
echo  RightClickResizer Build Script
echo ========================================
echo.

REM Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python.
    pause
    exit /b 1
)

echo [1/4] Installing requirements...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install requirements.
    pause
    exit /b 1
)
echo.

echo [2/4] Locating ffmpeg.exe...
set FFMPEG_PATH=C:\Users\Rohin\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg.Shared_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0-full_build-shared\bin\ffmpeg.exe

if not exist "%FFMPEG_PATH%" (
    echo WARNING: ffmpeg.exe not found at default location.
    echo Trying to find ffmpeg in PATH...
    where ffmpeg >nul 2>&1
    if %errorlevel% neq 0 (
        echo ERROR: ffmpeg not found. Please install ffmpeg first.
        echo Download from: https://ffmpeg.org/download.html
        pause
        exit /b 1
    )
)
echo Found: %FFMPEG_PATH%
echo.

echo [3/4] Building executable with embedded ffmpeg...
python -m PyInstaller ^
    --noconfirm ^
    --onefile ^
    --windowed ^
    --name "RightClickResizer" ^
    --icon "NONE" ^
    --add-data "%FFMPEG_PATH%;." ^
    src/main.py

if %errorlevel% neq 0 (
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo [4/4] Build complete!
echo.
echo ========================================
echo  Executable: dist\RightClickResizer.exe
echo ========================================
echo.
echo Next steps:
echo 1. Run dist\RightClickResizer.exe as Administrator
echo 2. Click "Install Context Menu"
echo 3. Right-click on images or videos to use
echo.
pause
