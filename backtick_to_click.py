# make it so pressing the backtick triggers a click so I don't have to use the mouse for certain tedious tasks in
# lightroom
import keyboard
import pyautogui


def click_mouse():
    pyautogui.click()


# Define the hotkey (backtick in this case) and the function to call
keyboard.add_hotkey("`", click_mouse)

# Keep the program running
keyboard.wait("esc")
