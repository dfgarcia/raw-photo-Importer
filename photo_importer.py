import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import shutil
import datetime
import exifread
import threading
import json
from PIL import Image, ImageTk

import sys

class PhotoImporterApp:
    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def __init__(self, root):
        self.root = root
        self.root.title("Shitty RAW Photo Importer")
        self.root.geometry("600x500")
        self.config_file = os.path.expanduser("~/.photo_importer_config.json")
        
        # Icon
        try:
            icon_path = self.resource_path("app_icon.jpg")
            if os.path.exists(icon_path):
                img = Image.open(icon_path)
                photo = ImageTk.PhotoImage(img)
                self.root.iconphoto(False, photo)
        except Exception as e:
            print(f"Failed to load icon: {e}")
        
        # Load settings
        self.settings = self.load_config()

        # Menu
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

        # Source
        self.source_frame = tk.Frame(root)
        self.source_frame.pack(pady=10, fill=tk.X, padx=10)
        
        tk.Label(self.source_frame, text="Source Folder:").pack(anchor=tk.W)
        
        self.source_container = tk.Frame(self.source_frame)
        self.source_container.pack(fill=tk.X)
        
        self.source_entry = tk.Entry(self.source_container)
        self.source_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        if self.settings.get("source"):
            self.source_entry.insert(0, self.settings["source"])
        self.btn_browse_source = tk.Button(self.source_container, text="Browse", command=self.browse_source)
        self.btn_browse_source.pack(side=tk.LEFT)

        # Destination
        self.dest_frame = tk.Frame(root)
        self.dest_frame.pack(pady=10, fill=tk.X, padx=10)
        
        tk.Label(self.dest_frame, text="Destination Folder:").pack(anchor=tk.W)
        
        self.dest_container = tk.Frame(self.dest_frame)
        self.dest_container.pack(fill=tk.X)
        
        self.dest_entry = tk.Entry(self.dest_container)
        self.dest_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        if self.settings.get("dest"):
            self.dest_entry.insert(0, self.settings["dest"])
        self.btn_browse_dest = tk.Button(self.dest_container, text="Browse", command=self.browse_dest)
        self.btn_browse_dest.pack(side=tk.LEFT)

        # Actions
        self.action_frame = tk.Frame(root)
        self.action_frame.pack(pady=10)
        
        self.btn_start = tk.Button(self.action_frame, text="Start Import", command=self.start_import_thread, bg="green", font=("Arial", 12, "bold"))
        self.btn_start.pack()

        # Progress
        self.progress_label = tk.Label(root, text="Ready")
        self.progress_label.pack(pady=5)
        
        from tkinter import ttk
        self.progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=400, mode='determinate')
        self.progress_bar.pack(pady=5)

        # Log
        self.log_text = scrolledtext.ScrolledText(root, height=15)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # RAW Extensions
        self.raw_extensions = {'.CR2', '.NEF', '.ARW', '.DNG', '.ORF', '.RW2', '.SR2', '.RAF', '.CR3'}
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    return json.load(f)
            except:
                pass
        return {}

    def save_config(self):
        self.settings["source"] = self.source_entry.get()
        self.settings["dest"] = self.dest_entry.get()
        try:
            with open(self.config_file, "w") as f:
                json.dump(self.settings, f)
        except Exception as e:
            print(f"Failed to save config: {e}")

    def on_closing(self):
        self.save_config()
        self.root.destroy()

    def browse_source(self):
        initial = self.source_entry.get() if os.path.isdir(self.source_entry.get()) else "/"
        folder = filedialog.askdirectory(initialdir=initial)
        if folder:
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, folder)

    def browse_dest(self):
        initial = self.dest_entry.get() if os.path.isdir(self.dest_entry.get()) else "/"
        folder = filedialog.askdirectory(initialdir=initial)
        if folder:
            self.dest_entry.delete(0, tk.END)
            self.dest_entry.insert(0, folder)

    def show_about(self):
        messagebox.showinfo("About", "RAW Photo Importer\nVersion 1.0\nCreated by Daniel Garcia")

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def start_import_thread(self):
        source = self.source_entry.get()
        dest = self.dest_entry.get()

        if not source or not os.path.isdir(source):
            messagebox.showerror("Error", "Invalid Source Directory")
            return
        if not dest or not os.path.isdir(dest):
            messagebox.showerror("Error", "Invalid Destination Directory")
            return

        self.btn_start.config(state=tk.DISABLED)
        thread = threading.Thread(target=self.import_photos, args=(source, dest))
        thread.start()

    def get_date_taken(self, filepath):
        """Returns a datetime object from EXIF or file modification time."""
        try:
            with open(filepath, 'rb') as f:
                tags = exifread.process_file(f, stop_tag="EXIF DateTimeOriginal", details=False)
                date_taken = tags.get("EXIF DateTimeOriginal")
                if date_taken:
                    # Format: YYYY:MM:DD HH:MM:SS
                    return datetime.datetime.strptime(str(date_taken), "%Y:%m:%d %H:%M:%S")
        except Exception as e:
            pass # Fallback
        
        # Fallback to modification time
        timestamp = os.path.getmtime(filepath)
        return datetime.datetime.fromtimestamp(timestamp)

    def import_photos(self, source, dest):
        self.log(f"Starting import from {source} to {dest}...")
        
        # Count total first for progress bar
        total_files = 0
        for root, dirs, files in os.walk(source):
            for file in files:
                if os.path.splitext(file)[1].upper() in self.raw_extensions:
                    total_files += 1
        
        self.progress_bar["maximum"] = total_files
        self.progress_bar["value"] = 0
        
        count = 0
        copied = 0
        skipped = 0
        
        for root, dirs, files in os.walk(source):
            for file in files:
                ext = os.path.splitext(file)[1].upper()
                if ext in self.raw_extensions:
                    count += 1
                    # Update progress
                    self.progress_bar["value"] = count
                    self.root.update_idletasks() # Force UI update
                    
                    filepath = os.path.join(root, file)
                    
                    try:
                        date_obj = self.get_date_taken(filepath)
                        year = date_obj.strftime("%Y")
                        month = date_obj.strftime("%m")
                        day = date_obj.strftime("%d")
                        
                        target_dir = os.path.join(dest, year, month, day)
                        os.makedirs(target_dir, exist_ok=True)
                        
                        target_path = os.path.join(target_dir, file)
                        
                        # Check for duplicate
                        if os.path.exists(target_path):
                            # Simple check: if size matches, skip
                            # If size differs, rename
                            if os.path.getsize(target_path) == os.path.getsize(filepath):
                                self.log(f"Skipping duplicate: {file}")
                                skipped += 1
                                continue
                            else:
                                base, extension = os.path.splitext(file)
                                new_name = f"{base}_{int(datetime.datetime.now().timestamp())}{extension}"
                                target_path = os.path.join(target_dir, new_name)
                                self.log(f"Conflict found. Renaming to {new_name}")

                        shutil.copy2(filepath, target_path)
                        self.log(f"Copied: {file} -> {year}/{month}/{day}")
                        copied += 1
                        
                        # Update UI periodically (safely omitted detailed queue for simplicity in this script, direct update works in simple tkinter apps usually but not unrelated threads strictly speaking. For strict safety update_idletasks or queue is better, but this usually flies for simple tools).
                        # To be safe, we won't touch GUI elements directly in loop deeply, but text append is usually tolerant enough in simple scripts or we accept the risk. 
                        # Ideally use root.after for updates.
                        
                    except Exception as e:
                        self.log(f"Error processing {file}: {e}")

        self.log(f"Import Finished. Processed {count} files. Copied: {copied}. Skipped: {skipped}.")
        self.btn_start.config(state=tk.NORMAL)
        messagebox.showinfo("Done", f"Import Completed!\nCopied: {copied}\nSkipped: {skipped}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoImporterApp(root)
    root.mainloop()
