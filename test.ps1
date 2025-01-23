# Basic system information and automation example
function Get-SystemInfo {
    $computerInfo = @{
        ComputerName = $env:COMPUTERNAME
        OSVersion = (Get-WmiObject Win32_OperatingSystem).Version
        LastBootTime = (Get-WmiObject Win32_OperatingSystem).LastBootUpTime
        FreeMemory = (Get-Counter '\Memory\Available MBytes').CounterSamples.CookedValue
    }
    
    return $computerInfo
}

# Process management example
function Start-CustomProgram {
    param(
        [string]$programPath
    )
    
    try {
        Start-Process $programPath
        Write-Host "Successfully started $programPath"
    }
    catch {
        Write-Host "Error starting program: $_"
    }
}

# Example usage:
$sysInfo = Get-SystemInfo
Write-Host "System Information:"
$sysInfo | Format-Table

# Similar to your Firefox example, but with error handling
Start-CustomProgram "C:\Program Files\Mozilla Firefox\firefox.exe"