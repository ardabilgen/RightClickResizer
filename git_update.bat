@echo off
set /p commit_msg="Commit mesaji girin (Enter basarsaniz 'Update' kullanilir): "
if "%commit_msg%"=="" set commit_msg=Update

echo Git guncelleniyor...
git add .
git commit -m "%commit_msg%"
git push

echo.
echo Islem tamamlandi.
pause
