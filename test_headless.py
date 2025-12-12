
import os
import shutil
import datetime
import sys

# Mocking the Tkinter and GUI parts for headless testing
# We will import the logic function directly if possible, 
# but since the logic is inside the class and tied to self.log, 
# it might be easier to just copy the logic here or subclass for testing.

from photo_importer import PhotoImporterApp
import tkinter as tk

class HeadlessImporter(PhotoImporterApp):
    def __init__(self):
        # Bypass GUI initialization
        self.raw_extensions = {'.CR2', '.NEF', '.ARW', '.DNG', '.ORF', '.RW2', '.SR2', '.RAF', '.CR3'}
        self.logs = []
        # Mock button, root, and progress bar
        self.btn_start = type('MockBtn', (), {'config': lambda *args, **kwargs: None})()
        self.root = type('MockRoot', (), {'update_idletasks': lambda *args, **kwargs: None})()
        self.progress_bar = {}

    def log(self, message):
        print(f"[LOG]: {message}")
        self.logs.append(message)
    
    # We re-use import_photos from the original class if it doesn't touch GUI too much.
    # The original import_photos calls self.log (overridden) and messagebox (problem).
    # We need to mock messagebox or avoid it. 
    # Actually, import_photos only uses messagebox at the end or start.
    # But start_import_thread calls messagebox. import_photos calls messagebox at end!
    
    # Let's override import_photos to avoid messagebox but keep logic OR just duplicate logic for safety if strict-mocking is hard.
    # Actually, let's just monkeypatch messagebox.
    
def mock_messagebox(*args, **kwargs):
    print(f"[MsgBox]: {args} {kwargs}")

import tkinter.messagebox
tkinter.messagebox.showinfo = mock_messagebox
tkinter.messagebox.showerror = mock_messagebox

if __name__ == "__main__":
    # Setup mock data first if not exists
    if not os.path.exists("mock_test/SD_CARD"):
        print("Run setup_mock.py first!")
        sys.exit(1)

    app = HeadlessImporter()
    
    source = os.path.abspath("mock_test/SD_CARD")
    dest = os.path.abspath("mock_test/Backup")
    
    print(f"Testing import from {source} to {dest}")
    app.import_photos(source, dest)
    
    # Verification
    expected_path = os.path.join(dest, "2023", "10", "15")
    if os.path.exists(expected_path):
        files = os.listdir(expected_path)
        print(f"Found files in {expected_path}: {files}")
        if len(files) >= 3: # We created 3 raw files
            print("SUCCESS: Files imported to correct date structure.")
        else:
            print("FAILURE: Missing files.")
    else:
        print(f"FAILURE: Directory {expected_path} not found.")

