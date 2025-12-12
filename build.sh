#!/bin/bash
# Clean previous builds
rm -rf build dist

# Run PyInstaller
/Users/danielgarcia/Antigravity/.venv/bin/pyinstaller --noconfirm --onefile --windowed --name "PhotoImporter" --add-data "app_icon.jpg:." --icon "app_icon.jpg" photo_importer.py

echo "Build complete. App is located in dist/PhotoImporter.app"
