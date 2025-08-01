import PyInstaller.__main__
import os

def build_executable():
    """Build the executable using PyInstaller"""
    
    # Define the build arguments (minimal, aggressive optimization)
    args = [
        '--onefile',
        '--windowed',
        '--name=TimesheetProcessor',
        '--hidden-import=fitz',
        '--clean',
        '--upx-dir=upx',  # assumes UPX is installed in ./upx or in PATH
        '--strip',
        'main.py'
    ]

    # Remove icon argument if icon file doesn't exist
    if not os.path.exists('icon.ico'):
        args = [arg for arg in args if not arg.startswith('--icon')]

    print("Building executable with PyInstaller (aggressively optimized)...")
    print("This may take a few minutes...")
    print("UPX compression will be used for smallest possible .exe.")

    try:
        PyInstaller.__main__.run(args)
        print("\n" + "="*50)
        print("BUILD SUCCESSFUL!")
        print("="*50)
        print(f"Executable created: dist/TimesheetProcessor.exe")
        print("\nThe application is now completely self-contained!")
        print("No external software installation required.")
        print("OCR capabilities are built into PyMuPDF.")
        print("UPX compression applied for minimal size.")
    except Exception as e:
        print(f"\nBuild failed: {str(e)}")
        return False

    return True

if __name__ == "__main__":
    build_executable()
