@echo off
echo Installing requirements...
pip install -r requirements.txt

echo Building executable...
python -m PyInstaller --noconfirm --onefile --windowed --name "RightClickResizer" --icon "NONE" src/main.py

echo Build complete. Executable is in dist/RightClickResizer.exe
pause
