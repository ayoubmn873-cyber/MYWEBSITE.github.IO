@echo off
set /p msg="Commit message (or press Enter for 'update'): "
if "%msg%"=="" set msg=update

git add .
git commit -m "%msg%"
git push

echo.
echo Done! Site published.
pause
