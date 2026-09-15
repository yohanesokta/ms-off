@echo off
set PATH=D:\Programs\MSYS\mingw64\bin;D:\Programs\MSYS\usr\bin;%PATH%
if not exist build mkdir build
gcc src\main.c -o build\msoff.exe -luser32
