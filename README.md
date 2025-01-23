# Windows Sub System (WSS) 

Prereqs: Qemu, KVM, perms, windows ISO file

1. Create VM disk
      
```qemu-img create -f qcow2 myvm.qcow2 60G```

2. Boot
      
```qemu-system-x86_64   -enable-kvm   -m 8096   -cpu host   -smp 4   -hda myvm.qcow2   -cdrom ~/Downloads/tiny.iso   -boot d``` 

3. Start

```qemu-system-x86_64   -enable-kvm   -m 6144   -cpu host   -smp 4   -hda myvm.qcow2   -boot c``` 

4. Have fun! If you ever break something you can always re-install using the boot d (floppy).
I tried getting WSL running and that wasnt a good idea.


----

I tested up to 8 and 10 vCPUs and my laptop barely broke the 40% CPU/ 50% RAM point using the Tiny11 install
Also does eat up quite a bit of ram but that was expected... On install it will break the 90%.

![Screenshot from 2025-01-22 03-54-26](https://github.com/user-attachments/assets/54353e1a-fde2-4465-abe5-6ec55060734e)

To share a drive with the guest machine:

      sudo apt-get install samba

```qemu-system-x86_64 -enable-kvm -m 6144 -cpu host -smp 8 -hda myvm.qcow2 -boot c -net nic -net user,smb=/home/hadepop/Desktop/vm/shared``` 

Then naviguate in file explorer to: ```  \\10.0.2.4\qemu ``` 

This way you don't even need clipboard share.

![image](https://github.com/user-attachments/assets/c256c442-0cf6-48d6-b8c7-562038389b09)

```  
import random

x = "Hello from Python in Windows on Linux"
#print(f'{x}')
y = random.choice(x)
print(f'{y}')

import sys

print(f"Exec: {sys.executable}")

## Use absolute paths as they are more likely not to change. 
import subprocess
#subprocess.run(['C:\\Program Files\\Mozilla Firefox\\firefox.exe'])

### Run powershell scripts directly
#subprocess.run(['powershell.exe', 'Start-Process firefox'])

## Simplest Hello World Search

import time
#import pyautogui as pag

#time.sleep(2)  # Wait for Firefox to open
#pag.write('Hello World')
#time.sleep(1)
#pag.press('enter')

```

If the whole set-up works it's very cool! 

You a truly on shared system between the Windows and Linux:

``` 
If you see this you're a G : (.venv) PS Microsoft.PowerShell.Core\FileSystem::\\10.0.2.4\qemu> 
```

On the guest system you will have to enable PS scripts in settings (Settings > Then type in the search bar Powershell)

Then run the script again and get output:
```
(.venv) PS Microsoft.PowerShell.Core\FileSystem::\\10.0.2.4\qemu> & //10.0.2.4/qemu/.venv/Scripts/python.exe //10.0.2.4/qemu/hello.py       
H
Exec: \\10.0.2.4\qemu\.venv\Scripts\python.exe
```  

If you got here congrats :)

If you didn't you might have to set ``` Set-ExecutionPolicy RemoteSigned``` 
You also have to launch this PowerShell admin. Yes the good things behind a single toggle or several... And a few downloads. 

![image](https://github.com/user-attachments/assets/68dd3dfc-7f01-4f79-98e9-a34f3e26cc36)

I don't know how safe any of this is in practice but since this is a VM set-up with a pirated iso... Well you get the idea. 

Now if you want to learn about Powershell commands the easiest way is simply to run a CMD and enter ISE.
This opens a graphical interface with every single command possible...

## For further Windows clean-up:

Settings > Privacy & Security > Search Permissions
Tick off everything but local search. 





