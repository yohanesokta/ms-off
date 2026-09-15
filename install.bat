@echo off
echo Mengekstrak Portable Python...
if not exist "runtimes\python\python.exe" (
    powershell -Command "Expand-Archive -Path 'runtimes\python.zip' -DestinationPath 'runtimes\python' -Force"
) else (
    echo Python sudah terekstrak, melewati proses ekstrak...
)

echo Menginstal Virtual Display Driver...
powershell -ExecutionPolicy Bypass -File "driver\Community Scripts\virtual-driver-manager.ps1" -Action install -Silent
