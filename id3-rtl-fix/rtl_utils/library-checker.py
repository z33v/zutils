"""
Dependency management and library installation utilities
"""

import sys
import subprocess
from importlib import import_module

def ensure_libraries_installed():
    """
    Check if required libraries are installed, if not, install them
    Returns a dictionary of imported modules
    """
    required_libraries = {
        'mutagen': 'Working with audio files and tags',
        'tqdm': 'Progress bar visualization'
    }
    
    missing_libraries = []
    imported_modules = {}
    
    for lib, purpose in required_libraries.items():
        try:
            imported_modules[lib] = import_module(lib)
            print(f"Found {lib} library")
        except ImportError:
            missing_libraries.append((lib, purpose))
    
    if missing_libraries:
        print("\nSome required libraries are missing. Installing...")
        for lib, purpose in missing_libraries:
            print(f"\nInstalling {lib} ({purpose})...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
                print(f"Successfully installed {lib}")
                
                # Import the newly installed library
                try:
                    imported_modules[lib] = import_module(lib)
                except ImportError as e:
                    print(f"Error importing {lib} after installation: {e}")
                    sys.exit(1)
            except subprocess.CalledProcessError as e:
                print(f"Error installing {lib}: {e}")
                print(f"Please install {lib} manually using: pip install {lib}")
                sys.exit(1)
        
        print("\nAll required libraries have been installed.")
    
    return True
