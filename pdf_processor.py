from PyPDF2 import PdfReader, PdfWriter
import fitz  # PyMuPDF
from PIL import Image
import io
import re
import pandas as pd
import zipfile
import os
import tempfile
from datetime import datetime


class PDFProcessor:
    def __init__(self):
        # Initialize OCR capability check
        self.ocr_available = self.check_ocr_support()
        
    def check_ocr_support(self):
        """Check if PyMuPDF supports OCR"""
        try:
            # PyMuPDF 1.23+ has built-in OCR via get_textpage_ocr()
            doc = fitz.open()  # Create empty document to test
            page = doc.new_page()  # Create a test page
            # Check if OCR method exists
            has_ocr = hasattr(page, 'get_textpage_ocr')
            doc.close()
            return has_ocr
        except Exception:
            return False
        
    def extract_text_with_ocr(self, pdf_path, log_callback=None):
        """Extract text from PDF using PyMuPDF's OCR capabilities"""
        try:
            if log_callback:
                log_callback(f"Extracting text with OCR: {os.path.basename(pdf_path)}")
            
            # Open PDF with PyMuPDF for text extraction
            doc = fitz.open(pdf_path)
            extracted_pages = []
            
            for page_num in range(len(doc)):
                if log_callback:
                    log_callback(f"Processing page {page_num+1}/{len(doc)} with OCR...")
                
                page = doc[page_num]
                
                # Try to extract text normally first
                text = page.get_text()
                
                # If no text found or very little text, try OCR
                if len(text.strip()) < 10:
                    try:
                        if self.ocr_available:
                            # Use PyMuPDF's OCR if available
                            # Note: get_textpage_ocr() might not be available in all PyMuPDF versions
                            # Fallback to enhanced text extraction
                            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                            # Try to get more text with higher resolution
                            text = page.get_text()
                            if len(text.strip()) < 5:
                                # If still no text, this might be a pure image PDF
                                text = f"[Image page - unable to extract text]"
                        else:
                            # Fallback: convert to image and try to extract more text
                            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                            # For now, just use the normal text extraction
                            text = page.get_text()
                    except Exception as ocr_error:
                        if log_callback:
                            log_callback(f"OCR failed for page {page_num+1}: {str(ocr_error)}")
                        text = page.get_text()  # Fallback to normal extraction
                
                extracted_pages.append({
                    'page_num': page_num + 1,
                    'text': text.strip()
                })
            
            doc.close()
            return extracted_pages
            
        except Exception as e:
            if log_callback:
                log_callback(f"Error in OCR processing: {str(e)}")
            raise
    
    def extract_text_regular(self, pdf_path, log_callback=None):
        """Extract text from PDF using regular text extraction"""
        try:
            if log_callback:
                log_callback(f"Extracting text from PDF: {os.path.basename(pdf_path)}")
            
            with open(pdf_path, 'rb') as file:
                reader = PdfReader(file)
                extracted_pages = []
                
                for i, page in enumerate(reader.pages):
                    text = page.extract_text() or ""
                    extracted_pages.append({
                        'page_num': i + 1,
                        'text': text.strip()
                    })
                    
                return extracted_pages
                
        except Exception as e:
            if log_callback:
                log_callback(f"Error in regular text extraction: {str(e)}")
            raise
    
    def extract_employee_name(self, text):
        """Extract employee name from text"""
        # Clean up whitespace
        text = re.sub(r"\s+", " ", text).strip()
        
        # Look for "for: [Name] DEN" pattern only
        match = re.search(r"(?<=for: ).*?(?= DEN)", text, re.IGNORECASE)
        if match:
            return match.group(0).strip()
        
        return ""
    
    def process_pdfs(self, pdf_files, options):
        """Main processing function"""
        try:
            progress_callback = options.get('progress_callback')
            log_callback = options.get('log_callback')
            ocr_enabled = options.get('ocr_enabled', True)
            create_zip = options.get('create_zip', True)
            output_folder = options.get('output_folder')
            
            total_files = len(pdf_files)
            all_rows = []
            
            if log_callback:
                log_callback(f"Starting to process {total_files} PDF files")
                log_callback(f"OCR enabled: {ocr_enabled}")
            
            # Process each PDF file
            for file_idx, pdf_path in enumerate(pdf_files):
                try:
                    if log_callback:
                        log_callback(f"Processing file {file_idx + 1}/{total_files}: {os.path.basename(pdf_path)}")
                    
                    # Update progress
                    base_progress = (file_idx / total_files) * 80  # 80% for processing files
                    if progress_callback:
                        progress_callback(base_progress, f"Processing {os.path.basename(pdf_path)}")
                    
                    # Extract text based on OCR setting
                    if ocr_enabled:
                        try:
                            pages_data = self.extract_text_with_ocr(pdf_path, log_callback)
                        except Exception as e:
                            if log_callback:
                                log_callback(f"OCR failed, falling back to regular extraction: {str(e)}")
                            pages_data = self.extract_text_regular(pdf_path, log_callback)
                    else:
                        pages_data = self.extract_text_regular(pdf_path, log_callback)
                    
                    # Process each page
                    previous_name = "Unknown"
                    for page_data in pages_data:
                        text = page_data['text']
                        page_num = page_data['page_num']
                        
                        # Extract employee name
                        name = self.extract_employee_name(text)
                        
                        # Fill down name if missing
                        if not name:
                            name = previous_name
                        else:
                            previous_name = name
                        
                        all_rows.append({
                            "Name": name,
                            "pageNum": page_num,
                            "Text": text,
                            "pdf_file": pdf_path
                        })
                        
                except Exception as e:
                    if log_callback:
                        log_callback(f"Error processing file {pdf_path}: {str(e)}")
                    # Continue with next file
                    continue
            
            if not all_rows:
                return {"success": False, "error": "No pages were successfully processed"}
            
            if progress_callback:
                progress_callback(85, "Grouping pages by employee...")
            
            # Group pages by employee
            df = pd.DataFrame(all_rows)
            if log_callback:
                log_callback(f"Found {len(df)} total pages")
                employees = df['Name'].unique()
                log_callback(f"Found employees: {', '.join(employees)}")
            
            grouped = df.groupby("Name")
            
            # Create output
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if create_zip:
                return self.create_zip_output(grouped, output_folder, timestamp, progress_callback, log_callback)
            else:
                return self.create_individual_pdfs(grouped, output_folder, timestamp, progress_callback, log_callback)
                
        except Exception as e:
            if log_callback:
                log_callback(f"Critical error in process_pdfs: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def create_zip_output(self, grouped, output_folder, timestamp, progress_callback, log_callback):
        """Create ZIP file with individual PDFs for each employee"""
        try:
            zip_filename = f"timesheets_by_employee_{timestamp}.zip"
            zip_path = os.path.join(output_folder, zip_filename)
            
            if log_callback:
                log_callback(f"Creating ZIP file: {zip_filename}")
            
            files_created = 0
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                total_employees = len(grouped)
                for emp_idx, (name, group) in enumerate(grouped):
                    if progress_callback:
                        progress = 85 + (emp_idx / total_employees) * 15
                        progress_callback(progress, f"Creating PDF for {name}")
                    
                    if log_callback:
                        log_callback(f"Creating PDF for employee: {name} ({len(group)} pages)")
                    
                    # Create PDF for this employee
                    writer = PdfWriter()
                    
                    # Group pages by PDF file to minimize file operations
                    file_groups = group.groupby('pdf_file')
                    
                    for pdf_file, file_group in file_groups:
                        try:
                            # Open the original PDF file fresh for each file group
                            with open(pdf_file, 'rb') as f:
                                reader = PdfReader(f)
                                
                                # Add pages from this file
                                for _, row in file_group.sort_values("pageNum").iterrows():
                                    page_num = row["pageNum"] - 1  # Convert to 0-based index
                                    if page_num < len(reader.pages):
                                        writer.add_page(reader.pages[page_num])
                                    else:
                                        if log_callback:
                                            log_callback(f"Warning: Page {page_num + 1} not found in {pdf_file}")
                        except Exception as e:
                            if log_callback:
                                log_callback(f"Error reading pages from {pdf_file}: {str(e)}")
                            continue
                    
                    if len(writer.pages) > 0:
                        # Create PDF in memory
                        pdf_buffer = io.BytesIO()
                        writer.write(pdf_buffer)
                        pdf_buffer.seek(0)
                        
                        # Create safe filename
                        safe_name = re.sub(r'[^\w\-_.]', '_', name)
                        filename = f"{safe_name}.pdf"
                        
                        # Add to ZIP
                        zipf.writestr(filename, pdf_buffer.getvalue())
                        pdf_buffer.close()
                        files_created += 1
                        if log_callback:
                            log_callback(f"✓ Created PDF for {name}")
                    else:
                        if log_callback:
                            log_callback(f"Warning: No pages found for employee {name}")
            
            if progress_callback:
                progress_callback(100, "Completed")
            
            if log_callback:
                log_callback(f"ZIP creation completed: {files_created} PDF files created")
            
            return {"success": True, "output_path": zip_path, "files_created": files_created}
            
        except Exception as e:
            if log_callback:
                log_callback(f"Error creating ZIP file: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def create_individual_pdfs(self, grouped, output_folder, timestamp, progress_callback, log_callback):
        """Create individual PDF files for each employee"""
        try:
            # Create subfolder for this batch
            batch_folder = os.path.join(output_folder, f"timesheets_{timestamp}")
            os.makedirs(batch_folder, exist_ok=True)
            
            if log_callback:
                log_callback(f"Creating individual PDFs in: {batch_folder}")
            
            created_files = []
            total_employees = len(grouped)
            
            for emp_idx, (name, group) in enumerate(grouped):
                if progress_callback:
                    progress = 85 + (emp_idx / total_employees) * 15
                    progress_callback(progress, f"Creating PDF for {name}")
                
                if log_callback:
                    log_callback(f"Creating PDF for employee: {name} ({len(group)} pages)")
                
                # Create PDF for this employee
                writer = PdfWriter()
                
                # Group pages by PDF file to minimize file operations
                file_groups = group.groupby('pdf_file')
                
                for pdf_file, file_group in file_groups:
                    try:
                        # Open the original PDF file fresh for each file group
                        with open(pdf_file, 'rb') as f:
                            reader = PdfReader(f)
                            
                            # Add pages from this file
                            for _, row in file_group.sort_values("pageNum").iterrows():
                                page_num = row["pageNum"] - 1  # Convert to 0-based index
                                if page_num < len(reader.pages):
                                    writer.add_page(reader.pages[page_num])
                                else:
                                    if log_callback:
                                        log_callback(f"Warning: Page {page_num + 1} not found in {pdf_file}")
                    except Exception as e:
                        if log_callback:
                            log_callback(f"Error reading pages from {pdf_file}: {str(e)}")
                        continue
                
                if len(writer.pages) > 0:
                    # Create safe filename
                    safe_name = re.sub(r'[^\w\-_.]', '_', name)
                    filename = f"{safe_name}.pdf"
                    file_path = os.path.join(batch_folder, filename)
                    
                    # Write PDF to file
                    try:
                        with open(file_path, 'wb') as output_file:
                            writer.write(output_file)
                        created_files.append(file_path)
                        if log_callback:
                            log_callback(f"✓ Created PDF for {name}")
                    except Exception as e:
                        if log_callback:
                            log_callback(f"Error writing PDF for {name}: {str(e)}")
                else:
                    if log_callback:
                        log_callback(f"Warning: No pages found for employee {name}")
            
            if progress_callback:
                progress_callback(100, "Completed")
            
            if log_callback:
                log_callback(f"Individual PDF creation completed: {len(created_files)} PDF files created")
            
            return {"success": True, "output_path": batch_folder, "files": created_files, "files_created": len(created_files)}
            
        except Exception as e:
            if log_callback:
                log_callback(f"Error creating individual PDFs: {str(e)}")
            return {"success": False, "error": str(e)}
