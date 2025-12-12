
import os
import time
import shutil

def create_mock_data():
    base_dir = "mock_test"
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
    os.makedirs(base_dir)
    
    source_dir = os.path.join(base_dir, "SD_CARD")
    dest_dir = os.path.join(base_dir, "Backup")
    os.makedirs(source_dir)
    os.makedirs(dest_dir)
    
    # Create fake RAW files
    # Note: These won't have EXIF, so they should fallback to File Modification Time
    
    files = ["IMG_001.CR2", "IMG_002.NEF", "video.mp4", "IMG_003.ARW"]
    
    for f in files:
        path = os.path.join(source_dir, f)
        with open(path, "w") as file:
            file.write("fake raw data")
        
        # Set a predictable mtime
        # Let's say: 2023-10-15
        date_time = time.mktime((2023, 10, 15, 12, 0, 0, 0, 0, 0))
        os.utime(path, (date_time, date_time))
        
    print(f"Created mock data in {base_dir}")
    print(f"Source: {os.path.abspath(source_dir)}")
    print(f"Dest: {os.path.abspath(dest_dir)}")

if __name__ == "__main__":
    create_mock_data()
