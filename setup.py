import subprocess
import sys
import os

def install_requirements():
    """Install required Python packages"""
    try:
        print("Installing Python packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Python packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install packages: {e}")
        return False

def check_dependencies():
    """Check if all Python dependencies are installed"""
    try:
        import fitz  # PyMuPDF
        print("✓ All Python dependencies are available")
        return True
    except ImportError as e:
        print(f"✗ Missing Python dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def main():
    print("Timesheet PDF Processor Setup")
    print("=" * 40)
    
    success = True
    
    # Install Python packages
    if not install_requirements():
        success = False
    
    print()
    
    # Check Python dependencies
    if not check_dependencies():
        success = False
    
    print()
    print("=" * 40)
    
    if success:
        print("✓ Setup completed successfully!")
        print("You can now run: python main.py")
    else:
        print("✗ Setup completed with errors")
        print("Please install missing dependencies before running the application")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
