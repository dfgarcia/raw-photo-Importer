#!/bin/bash
# Clean previous builds
rm -rf build dist

# Run PyInstaller
/Users/danielgarcia/Antigravity/.venv/bin/pyinstaller --noconfirm PhotoImporter.spec

echo "Build complete. App is located in dist/PhotoImporter.app"
