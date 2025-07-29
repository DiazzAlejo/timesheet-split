import PyInstaller.__main__
import os
import sys

def build_executable():
    """Build the executable using PyInstaller"""
    
    # Define the build arguments
    args = [
        '--onefile',                    # Create a single executable file
        '--windowed',                   # Don't show console window (GUI app)
        '--name=TimesheetProcessor',    # Name of the executable
        '--icon=icon.ico',              # Icon file (optional - you can create one)
        '--add-data=pdf_processor.py;.',# Include the processor module
        '--hidden-import=fitz',         # Ensure PyMuPDF is included
        '--hidden-import=PIL',          # Ensure PIL is included
        '--clean',                      # Clean PyInstaller cache and build folders
        'main.py'                       # Main script
    ]
    
    # Remove icon argument if icon file doesn't exist
    if not os.path.exists('icon.ico'):
        args = [arg for arg in args if not arg.startswith('--icon')]
    
    print("Building executable with PyInstaller...")
    print("This may take a few minutes...")
    
    try:
        PyInstaller.__main__.run(args)
        print("\n" + "="*50)
        print("BUILD SUCCESSFUL!")
        print("="*50)
        print(f"Executable created: dist/TimesheetProcessor.exe")
        print("\nThe application is now completely self-contained!")
        print("No external software installation required.")
        print("OCR capabilities are built into PyMuPDF.")
        
    except Exception as e:
        print(f"\nBuild failed: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    build_executable()
