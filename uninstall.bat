@echo off
echo Menghapus Virtual Display Driver...
powershell -ExecutionPolicy Bypass -File "driver\Community Scripts\virtual-driver-manager.ps1" -Action uninstall -Silent
echo Selesai! Driver telah dihapus dari sistem.
pause
