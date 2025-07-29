# Timesheet PDF Processor

A standalone Windows application that automatically splits timesheet PDFs by employee name, creating separate PDF files for each employee.

## 🚀 **Quick Download**

### **For End Users:**
1. Go to [**Releases**](../../releases)
2. Download `TimesheetProcessor.exe` from the latest release
3. Double-click to run - **no installation required!**

📖 **Need help?** See the [**User Guide**](USER_GUIDE.md) for detailed instructions.

---

## ✨ **Features**

- 🔍 **Smart Detection**: Finds employees using "for: [Employee Name] DEN" pattern
- 📄 **OCR Support**: Handles both text and scanned PDFs automatically
- 📦 **Batch Processing**: Process multiple PDF files at once
- 🗂️ **Organized Output**: Creates individual PDFs and ZIP archive
- 💻 **Standalone**: No Python or external software required (when using .exe)
- 📊 **Progress Tracking**: Real-time processing updates and logging

## 🎯 **What It Does**

**Input**: Timesheet PDFs containing multiple employees  
**Output**: Individual PDF files for each employee + ZIP archive

**Example**: 3 PDF files with 119 employees → 119 separate PDFs (one per employee)

## 🔧 **System Requirements**

### **For Standalone Executable:**
- **OS**: Windows 10/11
- **Memory**: 4GB RAM recommended for large files
- **Storage**: 500MB free space recommended
- **File Size**: 228MB download (includes everything needed)

### **For Python Development:**
- Python 3.8 or higher
- Windows OS (can be adapted for other platforms)

## 📋 **How to Use**

### **Option 1: Standalone Executable (Recommended)**
1. **Download**: Get `TimesheetProcessor.exe` from [Releases](../../releases)
2. **Run**: Double-click the executable
3. **Select Files**: Click "Add PDF Files" to choose your timesheet PDFs
4. **Choose Output**: Click "Browse" to select save location
5. **Process**: Click "Process PDFs" and wait for completion

**That's it!** No technical knowledge required.

### **Option 2: Run from Python Source**

#### Installation

```bash
pip install -r requirements.txt
```

This will install PyMuPDF, PyPDF2, Pandas, and other required packages.

#### Setup (Optional)

```bash
python setup.py
```

This will verify all dependencies are correctly installed.

#### Running the Application

```bash
python main.py
```

#### Using the GUI

1. **Add PDF Files**: Click "Add PDF Files" to select your timesheet PDFs
2. **Select Output Folder**: Choose where to save the processed files
3. **Configure Options**:
   - Enable/disable OCR processing
   - Choose to create ZIP file or individual PDFs
4. **Process**: Click "Process PDFs" to start processing

### Employee Name Detection

The application looks for employee names using this pattern:
- `for: [Employee Name] DEN`

You can modify the pattern in `pdf_processor.py` in the `extract_employee_name()` method.

## 🛠️ **For Developers**

### **Source Code Structure**
```
Timesheet/
├── main.py              # GUI application entry point
├── pdf_processor.py     # Core PDF processing and OCR engine
├── requirements.txt     # Python dependencies
├── build_exe.py        # Build script for creating executable
├── setup.py            # Dependency verification
├── USER_GUIDE.md       # End-user documentation
├── README.md           # This file
└── dist/               # Generated executables (after building)
```

### **Building Executable**

To create a standalone .exe file:

```bash
python build_exe.py
```

Or manually with PyInstaller:

```bash
pyinstaller --onefile --windowed --add-data "*.py;." main.py
```

### **Dependencies**
- PyPDF2 3.0.1: PDF manipulation
- PyMuPDF 1.24.5: OCR and text extraction
- Pandas 2.2.2: Data processing
- Tkinter: GUI framework (included with Python)
- PyInstaller 6.8.0: Executable creation

### **Employee Name Detection**

The application looks for employee names using this pattern:
- `for: [Employee Name] DEN`

You can modify the pattern in `pdf_processor.py` in the `extract_employee_name()` method.

## 📞 **Support**

### **Common Issues**
- **File not found**: Ensure PDFs contain "for: [Employee Name] DEN" pattern
- **Processing errors**: Check the log output for detailed error information
- **Large files**: Try processing smaller batches for better performance
- **OCR accuracy**: For better results, ensure PDFs have good image quality
- **Memory issues**: Process smaller batches of PDFs if you encounter memory errors

### **Getting Help**
1. Check the [User Guide](USER_GUIDE.md)
2. Review the processing log for error details
3. Open an issue with sample files (if possible)

## 📄 **License**

This project is open source. Feel free to use, modify, and distribute.

## 🏷️ **Tags**

`pdf-processing` `ocr` `timesheet` `automation` `windows` `standalone` `gui` `python`

---

**Latest Release**: v1.0.0 | **File Size**: 228MB | **Last Updated**: July 29, 2025
3. **Text extraction**: The app will try OCR if normal text extraction finds little content

### Error Messages

- `ImportError`: Install missing Python packages with `pip install -r requirements.txt`
- `Memory Error`: Try processing fewer files at once
- `File access errors`: Check file paths and permissions

## Customization

### Modifying Name Detection

Edit the `extract_employee_name()` method in `pdf_processor.py` to add custom patterns:

```python
def extract_employee_name(self, text):
    # Add your custom pattern here
    match = re.search(r"Your Pattern Here", text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    # ... existing patterns
```

### Adding New Features

The modular design makes it easy to add new features:
- Modify `PDFProcessor` class for new processing logic
- Update `TimesheetProcessorGUI` class for UI changes
- Add new options in the options dictionary

## License

This project is provided as-is for educational and internal use purposes.
