$unCryModDir = Join-Path $env:APPDATA "CryptoModule"
$unBSSDir = Join-Path $env:APPDATA "BSS\BSSPluginGPB"
$inCryModDir = "C:\temp"
$processName = "CryptoModule"
$processName1 = "javaw"

$banner = "=== GAZPROMBANK MODULE REINSTALLATION ==="
$width = [console]::WindowWidth
$padding = ($width - $banner.Length) / 2
Write-Host (" " * $padding) -NoNewline
Write-Host $banner -ForegroundColor Cyan
Write-Host ""

#1 Kill CryptoModule process

if (Get-Process -Name $processName -ErrorAction SilentlyContinue) {
    Write-Host "Terminating process $processName"
    Stop-Process -Name $ProcessName -Force
} else {
    Write-Host "Process $processName is not running"
}

#2 Kill Java process

if (Get-Process -Name $processName1 -ErrorAction SilentlyContinue) {
    Write-Host "Terminating process $processName1"
    Stop-Process -Name $ProcessName1 -Force
} else {
    Write-Host "Process $processName1 is not running"
}

#3 Uninstall CryptoModule

$unCryMod = Join-Path $unCryModDir "unins000.exe"
if (Test-Path $unCryMod) {
    Write-Host "Uninstalling Cryptomodule..."
    Start-Process -FilePath $unCryMod -ArgumentList "/verysilent", "/norestart" -Wait
} else {
    Write-Warning "Cryptomodule uninstaller not found"
}

#4 Uninstall BSS Plugin

$unBSS = Join-Path $unBSSDir "uninstall.exe"
if (Test-Path $unBSS) {
    Write-Host "Uninstalling BSS Plugin..."
    Start-Process -FilePath $unBSS -ArgumentList "--mode", "unattended" -Wait
} else {
    Write-Warning "BSS Plugin uninstaller not found"
}

#5 Install CryptoModule

$inCryMod = Join-Path $inCryModDir "cryptomodule.exe"
if (Test-Path $inCryMod) {
    Write-Host "Installing Cryptomodule..."
    Start-Process -FilePath $inCryMod -ArgumentList "/verysilent", "/norestart"
} else {
    Write-Warning "Cryptomodule installer not found"
}

Write-Host "Please wait 5 minutes for installation to complete..."
Start-Sleep -Seconds 300
Read-Host "GBO cryptomodule installed. Press Enter to continue"