from packagesInstaller.InstallExecutor import InstallExecutor
from packagesInstaller.LibraryInstallationInformation import LibraryInstallationInformation

from packagesInstaller.SetupPaths import libsDir, thirdPartyDir
from packagesInstaller.NativeToolsError import error

from packagesInstaller.BuildInstructionsParser import BuildInstructionsParser
from packagesInstaller.EnvironmentSetup import environmentConfiguration

from packagesInstaller.SystemDetection import win
from packagesInstaller.YamlConfigLoader import YamlConfigLoader

from typing import Deque
from packagesInstaller.generate.LibraryInstallationCommands import isLibrarySupported

import subprocess

class InstallationManager: 
    def __init__(
        self                :   'InstallationManager',
        silentInstallation  :   bool = False
    ) -> None:
        self.executorsQueue: Deque[InstallExecutor] = []
        self.silentInstallation: bool = silentInstallation

    def addInstallation(
        self:       'InstallationManager',
        name:       str, 
        location:   str = 'Libraries'
    ) -> None:
        if not isLibrarySupported(name):
            return
        
        if location == 'Libraries':
            directory: str = libsDir
        elif location == 'ThirdParty':
            directory: str = thirdPartyDir
        else:
            error('Unknown location: ' + location)

        libraryInstallationInformation: LibraryInstallationInformation = YamlConfigLoader.ExtractLibraryInformationFromYaml(name)

        commands: str = BuildInstructionsParser.FilterInstallationCommandsByPlatform(
            libraryInstallationInformation.installCommands).replace("LIB_BASE_INSTALLATION_DIRECTORY", directory)

        if len(commands) > 0:
            self.executorsQueue.append(
                InstallExecutor(
                    installationInformation=LibraryInstallationInformation(
                        libraryName=name, libraryInformation=libraryInstallationInformation.libraryInformation,
                        libraryVersion=libraryInstallationInformation.libraryVersion, 
                        installCommands=commands, location=location,
                        directory=directory, dependencies=libraryInstallationInformation.dependencies
                    ),
                  
                )
            )

    def executeAll(self: 'InstallationManager') -> None:
        if win:
            currentCodePage: str = subprocess.run('chcp',  
                capture_output=True, shell=True, text=True,
                env=environmentConfiguration.modifiedEnvironment).stdout.strip().split()[-1]
        
            subprocess.run('chcp 65001 > nul', shell=True, env=environmentConfiguration.modifiedEnvironment)
            self.__runStages()

            subprocess.run('chcp ' + currentCodePage + ' > nul', shell=True, env=environmentConfiguration.modifiedEnvironment)
        else:
            self.__runStages()

    def __runStages(self: 'InstallationManager') -> None:
        count = len(self.executorsQueue)
        index = 0

        for executor in self.executorsQueue:
            index = index + 1
            executor.install(queueLength=count, indexInQueue=index)
