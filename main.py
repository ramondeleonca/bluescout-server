import cv2
import tkinter as tk
import numpy as np
import tempfile
import uuid
import platform
import sys
import os
import utils
import json
import qrcode
import pandas as pd
from pyzbar import pyzbar
from typing import Literal
from constants import *
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont

FROZEN: bool = getattr(sys, 'frozen', False)
DIRNAME: str = sys._MEIPASS if FROZEN else os.path.dirname(os.path.realpath(__file__))
OS: Literal["linux", "windows", "darwin", "java"] = platform.system().lower()
TEMPDIR = tempfile.TemporaryDirectory(prefix=TEMP_DIR_PREFIX, suffix=uuid.uuid4().hex)
CAMERA = int(input("Camera index: "))

# Create a window and configure it
root = tk.Tk()
root.title(WINDOW_TITLE)
root.geometry(WINDOW_SIZE)

# Create the camera object
cap = cv2.VideoCapture(CAMERA)

# Create a label to display the camera feed
label = tk.Label(root)
label.pack()

qrs: list[pyzbar.Decoded] = []
update_loop_running: bool = False
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
        
        # Check for QR codes
        detected_qrs: list[pyzbar.Decoded] = pyzbar.decode(frame)
        
        # If there are any QR codes
        if len(detected_qrs) > 0:
            # Create a canvas from the image
            draw = ImageDraw.Draw(image)
            
            # Draw all qr codes
            for index, detected_qr in enumerate(detected_qrs):
                # Draw green if it's the first one, draw red if it's any other
                draw.polygon(
                    [(point.x, point.y) for point in detected_qr.polygon],
                    width=5,
                    outline=(0, 255, 0) if index == 0 else (255, 0, 0)
                )
            
            # Get the first QR code
            qr = detected_qrs[0]
            
            # Decode and parse the data
            try:
                # Try to parse the data
                data = utils.parse_csv_to_dict(qr.data.decode("utf-8"))
                
                # Check if it's a valid BlueScout QR code
                if "bs_qr_ver" in data:
                    on_qr_found(qr, data)
                    if not any(qr_item.data == qr.data for qr_item in qrs):
                        on_new_qr_found(qr, data)
                        qrs.append(qr)
            except:
                # If the data is invalid, draw it
                draw.text((qr.rect.left, qr.rect.top + qr.rect.height), "Invalid data format", fill=(255, 0, 0), font=ImageFont.truetype("arial.ttf", 20))
        
        # Convert it to a tkinter image
        photo = ImageTk.PhotoImage(image=image)
        
        # Update the label with the new image (I don't know why this works, just leave it alone)
        label.config(image=photo)
        label.image = photo

    # Call this function again after 10ms
    if update_loop_running:
        root.after(10, update_loop)

def on_qr_found(qr: pyzbar.Decoded, data: dict):
    print("qr found")

def on_new_qr_found(qr: pyzbar.Decoded, data: dict):
    print("new qr found")

try:
    update_loop_running = True
    update_loop()
    root.mainloop()
finally:
    cap.release()
    cv2.destroyAllWindows()
