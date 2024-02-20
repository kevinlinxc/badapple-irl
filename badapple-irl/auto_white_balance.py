# script to automatically use shortcuts on lightroom to set the white balance using the same spot in every photo
import keyboard
import pyautogui
import time

def perform_actions():
    for i in range(3104):
        pyautogui.press('right')  # Press right arrow key
        time.sleep(2)

        pyautogui.press('w')  # Press 'w' key
        time.sleep(0.5)

        pyautogui.click()  # Simulate a mouse click
        time.sleep(0.5)

# Flag to check if the actions are currently being performed
performing_actions = False

def toggle_actions():
    global performing_actions
    performing_actions = not performing_actions

    if performing_actions:
        print("Actions started. Press 'esc' to stop.")
        perform_actions()
    else:
        print("Actions stopped. Press Ctrl + ` to start again.")

# Define the hotkey (Ctrl + backtick) and the function to call
keyboard.add_hotkey('ctrl + `', toggle_actions)

# Keep the program running
keyboard.wait('esc')