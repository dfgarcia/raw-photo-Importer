# PhotoImporter

**Shitty RAW Photo Importer** is a simple Python application designed to organize your photography workflow. It copies RAW image files from a source directory (like an SD card) to a destination folder, automatically sorting them into a `YYYY/MM/DD` directory structure based on the photo's capture date.

## Features
- **RAW Support**: Handles common RAW formats including `.CR2`, `.NEF`, `.ARW`, `.DNG`, etc.
- **Date Organization**: Files are sorted into folders by year, month, and day.
- **EXIF Data**: accurate date extraction using EXIF metadata (falls back to file modification time if unavailable).
- **Duplicate Prevention**: Skips identical files and renames conflicts to avoid data loss.
- **Progress Tracking**: Visual progress bar and detailed activity logs.
- **Settings Persistence**: Remembers your last used folders.

## Installation & Running

### Prerequisites
- Python 3.x
- `pip`

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python photo_importer.py
```

## Building for macOS
You can package the application into a standalone `.app` bundle that does not require Python to be installed.

1. Run the build script:
    ```bash
    ./build.sh
    ```
2. The application will be created at `dist/PhotoImporter.app`.

## License
[MIT](LICENSE)
