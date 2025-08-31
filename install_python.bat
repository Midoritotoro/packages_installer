@echo off
setlocal

set PYTHON_INSTALL_PATH="C:/Python313"

for %%d in (%~dp0.) do set Directory=%%~fd
echo Directory=%Directory%

 :pythonExistanceCheck
   echo Checking for Python 3+ existance...
   :: where python >nul 2>&1

   :: if errorlevel 1 (
   ::    goto errorNoPython
   :: )

   if not exist "%PYTHON_INSTALL_PATH%" (
     goto errorNoPython
   )

   echo Python was found.
   goto startPackagesInstallation

 :errorNoPython
   echo.
   echo Python is not installed.
  
   echo Attempting to install python...
   goto :tryToInstallPython

 :tryToInstallPython
     PowerShell -NoProfile -ExecutionPolicy Bypass -File "%Directory%\powershell\InstallPython.ps1" -Verb RunAs
   
     if exist "%PYTHON_INSTALL_PATH%" (
         echo Python installation successful.
         goto startPackagesInstallation
         python -m "%Directory%\packagesInstaller" %*
     )
    
     echo Python installation failed. Stopping the build. 
     goto eof

 :startPackagesInstallation
     echo Installing Python packages...
     PowerShell -NoProfile -ExecutionPolicy Bypass -File "%Directory%\powershell\InstallPackagesInstallerRequirements.ps1" -Verb Runas

:eof
popd
endlocal
pause