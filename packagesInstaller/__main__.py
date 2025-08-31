from .InstallationManager import InstallationManager
from .generate.LibraryInstallationCommands import supportedLibraries

import argparse

if __name__ == "__main__":
    def main() -> None: 
        parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Script to install lib_base dependencies. ")

        parser.add_argument("--libraries", type=lambda s: s.split(','), default="all", help="Libraries to install. Default - all")
        parser.add_argument("--supported_libraries", action='store_true', help="Libraries supported for installation. ")
        
        parser.add_argument("--silent", action='store_true', help="Installation without information output, only error logs. ")
        parser.add_argument("--location", type=str, default="Libraries", help="Path to the folder where the libraries will be installed. ")
        
        args = parser.parse_args()

        if args.supported_libraries:
            print(', '.join(supportedLibraries))

        if not args.supported_libraries:
            libraries : list[str] = [lib.strip() for lib in args.libraries]
        
            if args.libraries[0] == "all":
                libraries = supportedLibraries

            manager: InstallationManager = InstallationManager(silentInstallation=args.silent)
            
            for library in libraries:
                manager.addInstallation(name=library, location=args.location)

            manager.executeAll() 

    main()