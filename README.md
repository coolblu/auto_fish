
# Minecraft Fishing Automation Script (Using Tesseract)

## Overview

This project is an automation script designed to fish automatically in Minecraft by detecting on-screen text using Tesseract OCR (Optical Character Recognition). It uses various Python libraries such as `pytesseract`, `pyautogui`, `opencv-python`, and `tkinter` to create a GUI, capture screen regions, detect specific text (like "Fish"), and simulate mouse clicks to automate the fishing process.

## Features

- **Automatic Fishing**: Detects subtitles like "Fish" and automatically clicks to reel in the fish.
- **Customizable Screen Region**: Users can update the screen region to focus on specific areas for subtitle detection.
- **Switching Water Bodies**: Moves the player to different water bodies after a set interval.
- **Debug Mode**: An overlay and console messages are displayed to assist with debugging.
- **Adjustable Delays**: Users can adjust the action delay and idle time limit for the automation process.
- **GUI Interface**: A simple Tkinter-based GUI allows easy control of the automation process.

## Requirements

Before running the script, ensure that the following dependencies are installed:

```bash
pip install pytesseract numpy pyautogui opencv-python pillow pywin32
```

Additionally, you must install Tesseract OCR on your system. On Windows, you can download it [here](https://github.com/tesseract-ocr/tesseract/wiki).

After installing, ensure that `pytesseract` can find the Tesseract executable by setting the path in the script:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OC\tesseract.exe'
```

## How to Run

1. **Install Tesseract**: 
   Ensure Tesseract is installed on your machine and the path is set correctly in the script.
   
2. **Launch the Script**: 
   Run the script using Python:

   ```bash
   python auto_fish.py
   ```

3. **Using the GUI**:
    - **Start**: Click the "Start" button to begin the fishing automation.
    - **Stop**: Click the "Stop" button to stop the automation.
    - **Debug Mode**: Toggle debug mode by clicking the "Debug: OFF" button, which will change to "Debug: ON" to enable debug messages and an overlay.
    - **Update Region**: Adjust the screen capture region by providing new values for top, left, width, and height, then click "Update Region."
    - **Action Delay**: Modify the action delay by entering a new delay in seconds and clicking "Update Action Delay."
    - **Idle Time Limit**: Update the idle time limit by entering a new value and clicking "Update Idle Time Limit."
    - **Switching Interval**: Set the time interval to switch between different water bodies.
    - **Move Duration**: Adjust the duration for moving between water bodies.

4. **Exiting the Program**:
   - To exit, click the "Exit" button or close the window.

## Customization

You can adjust several aspects of the fishing automation:

- **Region of Screen**: The default screen region for capturing subtitles is defined as:
  
  ```python
  region = {"top": 575, "left": 1450, "width": 500, "height": 375}
  ```
  This region can be updated via the GUI.

- **Action Delay**: The delay between automation actions is adjustable through the `action_delay` parameter.

- **Idle Time Limit**: The time limit before the fishing rod is automatically recast can be set through the `idle_time_limit` parameter.

- **Switching Interval**: The time interval (in minutes) after which the player switches to a new body of water can be set through the `switching_interval` parameter.

- **Move Duration**: The duration (in seconds) for which the player moves between water bodies can be adjusted using the `move_duration` parameter.

## Debug Mode

When enabled, debug mode:
- Displays a pink overlay around the screen capture region.
- Logs detected subtitles and fishing actions in a text box within the GUI.

## Known Issues

- This script is designed for systems running Windows due to the use of `win32api`, `win32con`, and `win32gui` libraries for the overlay. It may not be compatible with other operating systems.
- Ensure Minecraft is running in a windowed mode and that the subtitles are turned on for the automation to work.

## License

This project is open-source and available under the MIT License.

## Credits
https://github.com/UB-Mannheim/tesseract/wiki
This script uses:

- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) for text detection.
- [PyAutoGUI](https://github.com/asweigart/pyautogui) for automating mouse clicks.
- [OpenCV](https://opencv.org/) for image processing.
- [Tkinter](https://wiki.python.org/moin/TkInter) for GUI creation.

Feel free to contribute or modify the script for your needs!
