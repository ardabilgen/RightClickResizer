@echo off
echo Git kurulumu baslatiliyor...

git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/ardabilgen/RightClickResizer.git
git push -u origin main

echo.
echo Islem tamamlandi.
pause
