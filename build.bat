@echo off
REM Windows build script for Vedic Astrology Calculator

echo 🏗️  Windows Build Script
echo =======================

REM Create build directories
if not exist "dist" mkdir dist
if not exist "build" mkdir build

REM Install dependencies
echo 📦 Installing build dependencies...
if exist ".venv" (
    echo Using existing virtual environment...
    call .venv\Scripts\activate.bat
) else (
    echo Creating virtual environment...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    python -m pip install .
)

REM Install PyInstaller
python -m pip install pyinstaller

REM Build executable
echo 🔨 Building executable...
python build_executable.py

REM Create installer if NSIS is available
where makensis >nul 2>nul
if %errorlevel%==0 (
    echo 📦 Creating Windows installer...
    makensis installer.nsi
) else (
    echo ⚠️  NSIS not found, skipping installer creation
    echo    Install NSIS from https://nsis.sourceforge.io/
)

echo ✅ Build complete!
echo 📁 Files created in dist\ directory
pause