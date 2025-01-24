# Pip install keyboard pywin32 
# (CTRL + H to hide) 
## Uses a combination of PowerShell scripting + PyWin32 to perform actions on Windows

import keyboard
import subprocess
import win32gui
import win32con
import time

hidden_windows = []
is_hidden = False

def toggle_windows():
   global hidden_windows, is_hidden
   if not is_hidden:
       subprocess.run(['powershell.exe', '(New-Object -ComObject shell.application).toggleDesktop()'])
       time.sleep(0.3)
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

keyboard.add_hotkey('ctrl+h', toggle_windows)
keyboard.wait()
