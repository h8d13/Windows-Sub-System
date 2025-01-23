import subprocess
import json

def get_system_info():
    # PowerShell commands to get system info
    ps_commands = [
        "$env:COMPUTERNAME",
        "(Get-WmiObject Win32_OperatingSystem).Version",
        "(Get-WmiObject Win32_OperatingSystem).LastBootUpTime",
        "(Get-Counter '\\Memory\\Available MBytes').CounterSamples.CookedValue"
    ]
    
    computer_info = {}
    
    try:
        # Run each PowerShell command
        for i, cmd in enumerate(ps_commands):
            result = subprocess.run(['powershell', '-Command', cmd], 
                                 capture_output=True, text=True)
            if i == 0:
                computer_info['ComputerName'] = result.stdout.strip()
            elif i == 1:
                computer_info['OSVersion'] = result.stdout.strip()
            elif i == 2:
                computer_info['LastBootTime'] = result.stdout.strip()
            elif i == 3:
                computer_info['FreeMemory'] = result.stdout.strip()
    except Exception as e:
        print(f"Error getting system info: {e}")
    
    return computer_info

def start_custom_program(program_path):
    try:
        subprocess.run(['powershell', '-Command', f'Start-Process "{program_path}"'])
        print(f"Successfully started {program_path}")
    except Exception as e:
        print(f"Error starting program: {e}")

# Example usage
if __name__ == "__main__":
    sys_info = get_system_info()
    print("System Information:")
    for key, value in sys_info.items():
        print(f"{key}: {value}")
    
    # Start Firefox
    start_custom_program("C:\\Program Files\\Mozilla Firefox\\firefox.exe")