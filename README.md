# Windows Sub System (WSS) 

Prereqs: Qemu, KVM, perms, windows ISO file

1. Create VM disk
      
```qemu-img create -f qcow2 myvm.qcow2 60G```

2. Boot
      
```qemu-system-x86_64   -enable-kvm   -m 8096   -cpu host   -smp 4   -hda myvm.qcow2   -cdrom ~/Downloads/tiny.iso   -boot d``` 

3. Start

```qemu-system-x86_64   -enable-kvm   -m 6144   -cpu host   -smp 4   -hda myvm.qcow2   -boot c``` 

4. Have fun!

----

I tested up to 8 and 10 vCPUs and my laptop barely broke the 50% RAM point using the Tiny11 install
Also does eat up quite a bit of ram but that was expected...

![Screenshot from 2025-01-22 03-54-26](https://github.com/user-attachments/assets/54353e1a-fde2-4465-abe5-6ec55060734e)

Windows Sub System anyone? 

Because I know someone is going to try launch RDR2:

You might need to pass the USB:

        "-device", f"usb-host,hostbus={usb_device[0]},hostaddr={usb_device[1]}", 
        "-soundhw", "ac97",  
        "-audio-driver", "alsa",

To share a drive with the guest machine:
sudo apt-get install samba

        " qemu-system-x86_64 -enable-kvm -m 6144 -cpu host -smp 8 -hda myvm.qcow2 -boot c -net nic -net user,smb=/home/hadepop/Desktop/vm/shared"

Then naviguate in file explorer to \\10.0.2.4\qemu 

![image](https://github.com/user-attachments/assets/c256c442-0cf6-48d6-b8c7-562038389b09)

```  
import sys

print(f"System python: {sys.executable}")

#x = python -m venv venv
#y = python venv\Scripts\activate

## Use absolute paths as they are more likely not to change. 
import subprocess
subprocess.run(['C:\\Program Files\\Mozilla Firefox\\firefox.exe'])
``` 


