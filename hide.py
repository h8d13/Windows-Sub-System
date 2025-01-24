import keyboard
# Sets up listener for command
import subprocess
# To run powershell directly

import win32gui
import win32con
# For truly hiding a window

import time
# For .1 sleeps to ensure ooo 

# Config
# $command: ctrl+h

hidden_windows = []
# Remember what we've hidden
is_hidden = False
# Is it hidden

def toggle_windows():
   global hidden_windows, is_hidden
   if not is_hidden:
       subprocess.run(['powershell.exe', '(New-Object -ComObject shell.application).toggleDesktop()'])
       time.sleep(0.1)
       def callback(hwnd, _):
           if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
               win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
               hidden_windows.append(hwnd)
       win32gui.EnumWindows(callback, None)
       is_hidden = True
   else:
       for hwnd in hidden_windows:
           win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
       hidden_windows.clear()
       is_hidden = False

def task_view():
    import pyautogui as pag
    pag.hotkey('win', 'tab')  # Simulate Windows Key + Tab

keyboard.add_hotkey('ctrl+h', toggle_windows)
time.sleep(0.1)
keyboard.add_hotkey('ctrl+h', task_view)

keyboard.wait()
