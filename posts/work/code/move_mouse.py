import pyautogui

while True:
    cur_position = pyautogui.position()
    pyautogui.click(cur_position)
    pyautogui.sleep(300)
