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
        import pandas
        from PIL import Image
        print("✓ All Python dependencies are available")
        
        # Test PyMuPDF OCR support
        try:
            doc = fitz.open()
            page = doc.new_page()
            has_ocr = hasattr(page, 'get_textpage_ocr')
            doc.close()
            if has_ocr:
                print("✓ PyMuPDF OCR support available")
            else:
                print("⚠ PyMuPDF OCR not available (will use basic text extraction)")
            return True
        except Exception as e:
            print(f"⚠ PyMuPDF test failed: {e}")
            return True  # Still return True as basic functionality will work
            
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
        print("\nNote: EasyOCR will download language models (~50MB) on first use")
    else:
        print("✗ Setup completed with errors")
        print("Please install missing dependencies before running the application")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
