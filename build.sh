#!/bin/bash
# Cross-platform build script for Vedic Astrology Calculator

set -e

echo "🏗️  Cross-Platform Build Script"
echo "=================================="

# Detect platform
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m | tr '[:upper:]' '[:lower:]')

echo "🖥️  Platform: $OS ($ARCH)"

# Create build directory
mkdir -p dist
mkdir -p build

# Install dependencies
echo "📦 Installing build dependencies..."
if command -v uv &> /dev/null; then
    echo "Using uv..."
    export UV_PROJECT_ENVIRONMENT=.venv
    uv sync
    source .venv/bin/activate
elif command -v poetry &> /dev/null; then
    echo "Using Poetry..."
    poetry install
    source $(poetry env info --path)/bin/activate
else
    echo "Using pip..."
    python -m venv .venv
    source .venv/bin/activate
    python -m pip install .
fi

# Install PyInstaller
python -m pip install pyinstaller

# Build executable
echo "🔨 Building executable..."
python build_executable.py

# Platform-specific packaging
case $OS in
    darwin)
        echo "🍎 Creating macOS package..."
        if [ -d "dist/VedicAstrologyCalculator.app" ]; then
            hdiutil create -srcfolder "dist/VedicAstrologyCalculator.app" \
                          -format UDZO \
                          -fs HFS+ \
                          -volname "Vedic Astrology Calculator" \
                          "dist/VedicAstrologyCalculator.dmg" || true
        fi
        ;;
    linux)
        echo "🐧 Creating Linux packages..."
        # Create tar.gz
        if [ -d "dist/VedicAstrologyCalculator" ]; then
            tar -czf "dist/VedicAstrologyCalculator-linux-$ARCH.tar.gz" \
                -C dist VedicAstrologyCalculator
        fi
        ;;
esac

echo "✅ Build complete!"
echo "📁 Files created in dist/ directory"