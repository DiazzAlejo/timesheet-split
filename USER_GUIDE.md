# Timesheet PDF Processor - Standalone Application

## 📋 **What This Does**
This application automatically splits timesheet PDFs by employee name, creating separate PDF files for each employee.

## 🚀 **Quick Start**

### **For End Users (No Technical Setup Required)**

1. **Download**: Get the `TimesheetProcessor.exe` file
2. **Run**: Double-click `TimesheetProcessor.exe` to start
3. **Process**:
   - Click "Add PDF Files" to select your timesheet PDFs
   - Click "Browse" to choose where to save results
   - Click "Process PDFs" to start

**That's it!** No Python, no installations, no external software needed. Minimal dependencies, fastest startup, smallest download size.

## 📁 **What You Get**

- **ZIP File**: Contains individual PDF files for each employee
- **File Names**: Automatically generated from employee names
- **Processing Log**: Shows detailed progress and results

## 🎯 **Example**

**Input**: 3 PDF files with 119 employees
**Output**: 1 ZIP file containing 119 individual PDFs (one per employee)

## 💡 **Tips**

- **File Size**: The .exe is aggressively optimized and compressed (UPX, minimal dependencies)
- **Performance**: Can handle large PDFs with hundreds of pages
- **Employee Detection**: Looks for "for: [Employee Name] DEN" pattern
- **OCR Support**: Automatically handles scanned/image PDFs

## 🔧 **System Requirements**

- **OS**: Windows 10/11
- **Memory**: 4GB RAM recommended for large files
- **Disk Space**: 500MB free space recommended

## 📞 **Support**

If you encounter issues:
1. Check the processing log for error details
2. Try processing smaller batches of files
3. Ensure PDFs contain the expected employee name format

