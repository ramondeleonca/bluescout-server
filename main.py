import cv2
import tkinter as tk
import tempfile
import uuid
import platform
import sys
import os
import json
import schhemas
import threading
import lib.utils as utils
from lib.data_store import DataStore
from pyzbar import pyzbar
from typing import Literal
from constants import *
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont

# App Variables
# FROZEN: If the app is packaged with PyInstaller
# DIRNAME: The app entry file's directory
# OS: A string describing the operating system type
FROZEN: bool = getattr(sys, 'frozen', False)
DIRNAME: str = sys._MEIPASS if FROZEN else os.path.dirname(os.path.realpath(__file__))
OS: Literal["linux", "windows", "darwin", "java"] = platform.system().lower()

# Load configuration
# Loads defaultconfig.ini first
# Replaces available variables with config.ini
config = utils.load_config(os.path.join(DIRNAME, "defaultconfig.ini"), os.path.join(DIRNAME, "config.ini"))

# Setting variables
CAMERA: int = config.getint("SCANNER", "camera")
DATA_PATH: str = os.path.expandvars(config.get("PATHS", "data_path"))
APP_PATH: str = os.path.expandvars(config.get("PATHS", "app_path"))
TEMP_PATH: str = os.path.expandvars(config.get("PATHS", "temp_path"))

# If the paths arent found, rebuild the directory tree
if not os.path.exists(APP_PATH):
    print("Rebuilding app directory tree")
    os.makedirs(APP_PATH)

if not os.path.exists(TEMP_PATH):
    print("Rebuilding temp directory tree")
    os.makedirs(TEMP_PATH)

if not os.path.exists(DATA_PATH):
    print("Rebuilding data directory tree")
    os.makedirs(DATA_PATH)

# Make a temporary directory for the app
print("Creating temporary directory")
TEMPDIR = tempfile.TemporaryDirectory(dir=TEMP_PATH, prefix=TEMP_DIR_PREFIX, suffix=uuid.uuid4().hex)

# Create a Data Store object
print("Creating data store")
data_store = DataStore(DATA_PATH)

# Load stored data
print("Loading stored data")
threading.Thread(target=data_store.load, daemon=True).start()

# Create a window and configure it
root = tk.Tk()
root.title(WINDOW_TITLE)
root.geometry(WINDOW_SIZE)

# Create a label to display the camera feed
image_preview = tk.Label(root)
image_preview.pack()

# Create a button to commit the data to the database
commit_button = ttk.Button(root, text="Commit")
commit_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
commit_button.pack()

# Create the camera object
cap = cv2.VideoCapture(CAMERA)

qrs: list[pyzbar.Decoded] = []
def update_loop():
    # Global vars
    global cap
    
    # Read the new frame from the camera
    ret, frame = cap.read()
    
    # If the frame was read successfully
    if ret:
        # Convert it to RGB and resize it
        frame = cv2.resize(frame, (IMAGE_WIDTH, IMAGE_HEIGHT))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Convert it to a PIL image
        image = Image.fromarray(frame)
        
        # QR Reading optimizations
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        frame = cv2.convertScaleAbs(frame, alpha=1.5, beta=0)
        
        # Check for QR codes
        detected_qrs: list[pyzbar.Decoded] = pyzbar.decode(frame)
        
        # If there are any QR codes
        if len(detected_qrs) > 0:
            # Create a canvas from the image
            draw = ImageDraw.Draw(image, "RGBA")
            
            # Draw all qr codes
            for index, detected_qr in enumerate(detected_qrs):
                # Draw green if it's the first one, draw red if it's any other
                if detected_qr.polygon and len(detected_qr.polygon) >= 2:
                    try:
                        draw.polygon(
                            [(point.x, point.y) for point in detected_qr.polygon],
                            width=5,
                            outline=(0, 255, 0) if index == 0 else (255, 0, 0)
                        )
                    except:
                        print("Can't draw")
            
            # Get the first QR code
            qr = detected_qrs[0]
            
            # Decode and parse the data
            try:
                # Try to parse the data
                qr_text = qr.data.decode("utf-8")
                data = json.loads(qr_text)
                
                # Check if it's a valid BlueScout QR code
                if schhemas.bs_qr_code.is_valid(data):
                    try:
                        draw.text((qr.rect.left, qr.rect.top + qr.rect.height), qr_text, fill=(255, 0, 0), font=ImageFont.truetype("arial.ttf", 20))
                    except:
                        print("Can't draw QR text")
                    on_qr_found(qr, data)
                    if not any(qr_item.data == qr.data for qr_item in qrs):
                        on_new_qr_found(qr, data)
                        qrs.append(qr)
                    
            except:
                # If the data is invalid, draw it
                try:
                    draw.text((qr.rect.left, qr.rect.top + qr.rect.height), "Invalid data format", fill=(255, 0, 0), font=ImageFont.truetype("arial.ttf", 20))
                except:
                    print("Can't draw invalid data notice")
        
        # Convert it to a tkinter image
        photo = ImageTk.PhotoImage(image=image)
        
        # Update the label with the new image (I don't know why this works, just leave it alone)
        image_preview.config(image=photo)
        image_preview.image = photo

    # Call this function again after 10ms
    root.after(10, update_loop)

def on_qr_found(qr: pyzbar.Decoded, data: dict):
    pass

def on_new_qr_found(qr: pyzbar.Decoded, data: dict):
    data_store.add_unique(data)
    print("new qr found", data)

def main():
    try:
        update_loop()
        root.mainloop()
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    #! REMOVE THIS IN PRODUCTION
    # data_store.clear()
    main()