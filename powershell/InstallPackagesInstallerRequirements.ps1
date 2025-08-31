$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Path to build folder
$buildDir = (Get-Item $scriptDir).Parent.Parent.FullName

# Path to packagesInstaller folder
$packagesInstallerDir = Join-Path $buildDir "\packages_installer\packagesInstaller\"

# Paths to virtual environment and activation script
$venvPath = Join-Path $packagesInstallerDir "venv"
$activateScript = Join-Path $venvPath "\Scripts\Activate.bat"

Function Create-PythonVenv {
    Write-Host "Creating Python venv at $venvPath..."
    Start-Process "C:/Python313/python.exe" -Wait -ArgumentList "-m", "venv", $venvPath
    Write-Host "Activating Python venv..."
    & $activateScript
}

Function Python-InstallRequirements {
    $requirementsPath = Join-Path $buildDir "\packages_installer\requirements.txt"
    $newPythonPath = Join-Path $venvPath "\Scripts\python.exe"
    Write-Host "Installing requirements from $requirementsPath..."
    Start-Process $newPythonPath -Wait -ArgumentList "-m", "pip", "install", "-r", $requirementsPath
}

Create-PythonVenv
Python-InstallRequirements