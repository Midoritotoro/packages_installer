from packagesInstaller.SystemDetection import win, win64

from packagesInstaller.NativeToolsError import finish, executePath
from packagesInstaller.Getch import getch

import pathlib

import os
import sys


sys.dont_write_bytecode = True
scriptPath: str = os.path.dirname(os.path.realpath(__file__))

sys.path.append(scriptPath + '/..')
os.chdir(scriptPath + '/../../../..')

pathSep: str = ';' if win else ':'
libsLoc: str = 'Libraries' if not win64 else (os.path.join('Libraries', 'win64'))
keysLoc: str = 'cache_keys'

rootDir: str = os.getcwd()
libsDir: str = os.path.realpath(os.path.join(rootDir, libsLoc))
thirdPartyDir: str = os.path.realpath(os.path.join(rootDir, 'ThirdParty'))

usedPrefix: str = os.path.realpath(os.path.join(libsDir, 'local'))

if not os.path.isdir(os.path.join(libsDir, keysLoc)):
    pathlib.Path(os.path.join(libsDir, keysLoc)).mkdir(parents=True, exist_ok=True)

pathPrefixes: list[str] = [
    'ThirdParty\\msys64\\mingw64\\bin',
    'ThirdParty\\jom',
    'ThirdParty\\cmake\\bin',
    'ThirdParty\\gyp',
] if win else [
    'ThirdParty/gyp',
    'ThirdParty/yasm',
    'ThirdParty/depot_tools',
]

pathPrefix: str = ''
for singlePrefix in pathPrefixes:
    pathPrefix = pathPrefix + os.path.join(rootDir, singlePrefix) + pathSep

def removeDir(folder: str):
    if win:
        return 'if exist ' + folder + ' rmdir /Q /S ' + folder + '\nif exist ' + folder + ' exit /b 1'
    return 'rm -rf ' + folder