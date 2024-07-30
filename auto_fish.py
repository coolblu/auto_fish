import easyocr
import numpy as np
import pyautogui
import time
import threading
import tkinter as tk
from tkinter import messagebox
from PIL import ImageGrab
import os
import win32api
import win32con
import win32gui

# Initialize pyautogui
pyautogui.FAILSAFE = False

# Set the model folder for easyocr
model_storage_directory = os.path.join(os.path.dirname(__file__), 'easyocr_models')
print(f"Model storage directory: {model_storage_directory}")
reader = easyocr.Reader(['en'], model_storage_directory=model_storage_directory)

# Define the region of the screen to capture (default bottom right part of the screen)
region = {"top": 800, "left": 1200, "width": 300, "height": 100}

# Global variables to control the fishing automation and debug mode
running = False
debug = False
overlay_thread = None
stop_overlay_event = threading.Event()
action_delay = 1.0  # Delay between actions
idle_time_limit = 10  # Idle time limit in seconds

def capture_screen(region):
    # Capture a region of the screen
    screenshot = ImageGrab.grab(bbox=(region["left"], region["top"], region["left"] + region["width"], region["top"] + region["height"]))
    return np.array(screenshot)

def read_subtitles(image):
    # Use EasyOCR to do OCR on the image
    results = reader.readtext(image, detail=0)
    return ' '.join(results)

def log_message(message):
    log_text.config(state=tk.NORMAL)
    log_text.insert(tk.END, message + '\n')
    log_text.config(state=tk.DISABLED)
    log_text.yview(tk.END)  # Scroll to the end

def create_overlay_window():
    def on_paint(hwnd, msg, wp, lp):
        hdc, paint_struct = win32gui.BeginPaint(hwnd)
        rect = win32gui.GetClientRect(hwnd)
        brush = win32gui.CreateSolidBrush(win32api.RGB(255, 192, 203))  # Pink color
        win32gui.FrameRect(hdc, rect, brush)
        win32gui.EndPaint(hwnd, paint_struct)
        return 0  # Return 0 to indicate the message was processed

    wc = win32gui.WNDCLASS()
    wc.lpfnWndProc = on_paint
    wc.lpszClassName = 'OverlayWindow'
    wc.hbrBackground = win32con.HOLLOW_BRUSH
    wc.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW

    class_atom = win32gui.RegisterClass(wc)
    hwnd = win32gui.CreateWindowEx(
        win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_TOPMOST,
        class_atom,
        'Overlay',
        win32con.WS_POPUP,
        region['left'], region['top'], region['width'], region['height'],
        None, None, None, None
    )
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0, 0, 0), 0, win32con.LWA_COLORKEY)
    win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
    win32gui.UpdateWindow(hwnd)

    while not stop_overlay_event.is_set():
        win32gui.PumpWaitingMessages()

    win32gui.DestroyWindow(hwnd)
    win32gui.UnregisterClass(wc.lpszClassName, None)

def show_debug_overlay():
    global overlay_thread, stop_overlay_event
    if overlay_thread is None:
        stop_overlay_event.clear()
        overlay_thread = threading.Thread(target=create_overlay_window)
        overlay_thread.start()

def hide_debug_overlay():
    global overlay_thread, stop_overlay_event
    if overlay_thread is not None:
        stop_overlay_event.set()
        overlay_thread.join()
        overlay_thread = None

def refresh_overlay():
    if debug:
        hide_debug_overlay()
        show_debug_overlay()

def automate_fishing():
    global running, debug, idle_time_limit
    last_action_time = time.time()
    
    while running:
        start_time = time.time()
        # Capture the screen region
        screen_region = capture_screen(region)

        # Read subtitles from the screen region
        subtitles = read_subtitles(screen_region)
        
        if debug:
            log_message(f"Detected subtitles: {subtitles}")

        # Check if the subtitles contain "Fishing Bobber splashes"
        if "Fishing Bobber splashes" in subtitles:
            # Simulate right mouse click to reel in the fish
            pyautogui.click(button='right')
            last_action_time = time.time()  # Reset the last action time
            if debug:
                log_message("Fishing Bobber splashes detected, clicked the mouse to reel in the fish")

            # Wait for the action delay to ensure the subtitle disappears
            time.sleep(action_delay)

            # Recast the fishing rod
            pyautogui.click(button='right')
            last_action_time = time.time()  # Reset the last action time again
            if debug:
                log_message("Recast the fishing rod")
        elif time.time() - last_action_time > idle_time_limit:
            # If no target subtitle detected for the idle time limit, recast the fishing rod
            pyautogui.click(button='right')
            last_action_time = time.time()  # Reset the last action time
            if debug:
                log_message(f"No target subtitle detected for {idle_time_limit} seconds, recast the fishing rod")

        # Add a small delay to avoid excessive CPU usage and to maintain timing accuracy
        # elapsed_time = time.time() - start_time
        # time.sleep(max(0.1 - elapsed_time, 0))

def start_fishing():
    global running
    if not running:
        running = True
        threading.Thread(target=automate_fishing).start()
        start_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)

def stop_fishing():
    global running
    if running:
        running = False
        start_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)

def toggle_debug():
    global debug
    debug = not debug
    if debug:
        debug_button.config(text="Debug: ON")
        show_debug_overlay()
    else:
        debug_button.config(text="Debug: OFF")
        hide_debug_overlay()

def on_exit():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        stop_fishing()
        hide_debug_overlay()
        root.destroy()

def update_region():
    global region
    try:
        region = {
            "top": int(top_entry.get()),
            "left": int(left_entry.get()),
            "width": int(width_entry.get()),
            "height": int(height_entry.get())
        }
        log_message(f"Updated region: {region}")
        refresh_overlay()
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid integers for the region coordinates and dimensions.")

def update_action_delay():
    global action_delay
    try:
        action_delay = float(action_delay_entry.get())
        log_message(f"Updated action delay: {action_delay}")
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a valid number for the action delay.")

def update_idle_time_limit():
    global idle_time_limit
    try:
        idle_time_limit = float(idle_time_limit_entry.get())
        log_message(f"Updated idle time limit: {idle_time_limit}")
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a valid number for the idle time limit.")

# Create the GUI
root = tk.Tk()
root.title("Minecraft Fishing Automation")

start_button = tk.Button(root, text="Start", command=start_fishing)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop", command=stop_fishing, state=tk.DISABLED)
stop_button.pack(pady=10)

debug_button = tk.Button(root, text="Debug: OFF", command=toggle_debug)
debug_button.pack(pady=10)

# Add fields to update the region
region_frame = tk.Frame(root)
region_frame.pack(pady=10)

tk.Label(region_frame, text="Top:").grid(row=0, column=0)
top_entry = tk.Entry(region_frame)
top_entry.grid(row=0, column=1)
top_entry.insert(0, region['top'])

tk.Label(region_frame, text="Left:").grid(row=1, column=0)
left_entry = tk.Entry(region_frame)
left_entry.grid(row=1, column=1)
left_entry.insert(0, region['left'])

tk.Label(region_frame, text="Width:").grid(row=2, column=0)
width_entry = tk.Entry(region_frame)
width_entry.grid(row=2, column=1)
width_entry.insert(0, region['width'])

tk.Label(region_frame, text="Height:").grid(row=3, column=0)
height_entry = tk.Entry(region_frame)
height_entry.grid(row=3, column=1)
height_entry.insert(0, region['height'])

update_region_button = tk.Button(region_frame, text="Update Region", command=update_region)
update_region_button.grid(row=4, columnspan=2)

# Add field to update the action delay
action_delay_frame = tk.Frame(root)
action_delay_frame.pack(pady=10)

tk.Label(action_delay_frame, text="Action Delay (s):").grid(row=0, column=0)
action_delay_entry = tk.Entry(action_delay_frame)
action_delay_entry.grid(row=0, column=1)
action_delay_entry.insert(0, action_delay)

update_action_delay_button = tk.Button(action_delay_frame, text="Update Action Delay", command=update_action_delay)
update_action_delay_button.grid(row=1, columnspan=2)

# Add field to update the idle time limit
idle_time_limit_frame = tk.Frame(root)
idle_time_limit_frame.pack(pady=10)

tk.Label(idle_time_limit_frame, text="Idle Time Limit (s):").grid(row=0, column=0)
idle_time_limit_entry = tk.Entry(idle_time_limit_frame)
idle_time_limit_entry.grid(row=0, column=1)
idle_time_limit_entry.insert(0, idle_time_limit)

update_idle_time_limit_button = tk.Button(idle_time_limit_frame, text="Update Idle Time Limit", command=update_idle_time_limit)
update_idle_time_limit_button.grid(row=1, columnspan=2)

exit_button = tk.Button(root, text="Exit", command=on_exit)
exit_button.pack(pady=10)

log_text = tk.Text(root, state=tk.DISABLED, height=10, width=50)
log_text.pack(pady=10)

root.protocol("WM_DELETE_WINDOW", on_exit)

print("Starting the GUI event loop")
root.mainloop()
print("GUI event loop ended")
