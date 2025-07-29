import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys
from pdf_processor import PDFProcessor


class TimesheetProcessorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Timesheet PDF Processor")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.pdf_files = []
        self.output_folder = ""
        self.processor = PDFProcessor()
        
        self.setup_ui()
        self.check_ocr_status()
        
    def check_ocr_status(self):
        """Check OCR initialization status"""
        def check_status():
            try:
                if self.processor.ocr_available:
                    self.ocr_status_var.set("OCR Status: Ready ✓")
                else:
                    self.ocr_status_var.set("OCR Status: Basic text extraction only")
            except Exception as e:
                self.ocr_status_var.set(f"OCR Status: Error - {str(e)[:30]}...")
        
        # Run status check in background thread
        import threading
        thread = threading.Thread(target=check_status)
        thread.daemon = True
        thread.start()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Timesheet PDF Processor", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # File selection section
        file_frame = ttk.LabelFrame(main_frame, text="Select PDF Files", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(0, weight=1)
        
        # PDF files listbox
        self.files_listbox = tk.Listbox(file_frame, height=4)
        self.files_listbox.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # File buttons
        ttk.Button(file_frame, text="Add PDF Files", 
                  command=self.add_pdf_files).grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        ttk.Button(file_frame, text="Clear Files", 
                  command=self.clear_files).grid(row=1, column=1, sticky=tk.W)
        
        # Output folder section
        output_frame = ttk.LabelFrame(main_frame, text="Output Settings", padding="10")
        output_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        output_frame.columnconfigure(1, weight=1)
        
        ttk.Label(output_frame, text="Output Folder:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.output_var = tk.StringVar()
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_var, state='readonly')
        self.output_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        ttk.Button(output_frame, text="Browse", 
                  command=self.select_output_folder).grid(row=0, column=2)
        
        # OCR settings
        ocr_frame = ttk.LabelFrame(main_frame, text="OCR Settings", padding="10")
        ocr_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.ocr_enabled = tk.BooleanVar(value=True)
        ttk.Checkbutton(ocr_frame, text="Enable OCR Processing (EasyOCR)", 
                       variable=self.ocr_enabled).grid(row=0, column=0, sticky=tk.W)
        
        # OCR status label
        self.ocr_status_var = tk.StringVar(value="OCR Status: Ready")
        self.ocr_status_label = ttk.Label(ocr_frame, textvariable=self.ocr_status_var, 
                                         font=('Arial', 8))
        self.ocr_status_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        # Processing options
        options_frame = ttk.LabelFrame(main_frame, text="Processing Options", padding="10")
        options_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.create_zip = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Create ZIP file", 
                       variable=self.create_zip).grid(row=0, column=0, sticky=tk.W)
        
        # Process button
        self.process_button = ttk.Button(main_frame, text="Process PDFs", 
                                       command=self.start_processing, style='Accent.TButton')
        self.process_button.grid(row=5, column=0, columnspan=3, pady=20)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                          maximum=100, mode='determinate')
        self.progress_bar.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var)
        self.status_label.grid(row=7, column=0, columnspan=3)
        
        # Log area
        log_frame = ttk.LabelFrame(main_frame, text="Processing Log", padding="10")
        log_frame.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(8, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, state='disabled')
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def add_pdf_files(self):
        files = filedialog.askopenfilenames(
            title="Select PDF Files",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        for file in files:
            if file not in self.pdf_files:
                self.pdf_files.append(file)
                self.files_listbox.insert(tk.END, os.path.basename(file))
        
    def clear_files(self):
        self.pdf_files.clear()
        self.files_listbox.delete(0, tk.END)
        
    def select_output_folder(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder = folder
            self.output_var.set(folder)
            
    def log_message(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        self.root.update_idletasks()
        
    def update_progress(self, value, status=""):
        self.progress_var.set(value)
        if status:
            self.status_var.set(status)
        self.root.update_idletasks()
        
    def start_processing(self):
        if not self.pdf_files:
            messagebox.showerror("Error", "Please select at least one PDF file.")
            return
            
        if not self.output_folder:
            messagebox.showerror("Error", "Please select an output folder.")
            return
            
        # Disable the process button during processing
        self.process_button.config(state='disabled')
        self.progress_var.set(0)
        
        # Clear log
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')
        
        # Start processing in a separate thread
        thread = threading.Thread(target=self.process_pdfs)
        thread.daemon = True
        thread.start()
        
    def process_pdfs(self):
        try:
            self.log_message("Starting PDF processing...")
            
            # Set processing options
            options = {
                'ocr_enabled': self.ocr_enabled.get(),
                'create_zip': self.create_zip.get(),
                'output_folder': self.output_folder,
                'progress_callback': self.update_progress,
                'log_callback': self.log_message
            }
            
            # Process PDFs
            result = self.processor.process_pdfs(self.pdf_files, options)
            
            if result['success']:
                self.log_message(f"Processing completed successfully!")
                self.log_message(f"Output saved to: {result['output_path']}")
                
                # Display file count information
                files_created = result.get('files_created', 0)
                self.log_message(f"Total files created: {files_created}")
                
                self.update_progress(100, "Completed")
                
                # Enhanced success message with file count
                success_msg = f"Processing completed!\nOutput saved to: {result['output_path']}\nFiles created: {files_created}"
                messagebox.showinfo("Success", success_msg)
            else:
                self.log_message(f"Processing failed: {result['error']}")
                self.update_progress(0, "Failed")
                messagebox.showerror("Error", f"Processing failed: {result['error']}")
                
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self.log_message(error_msg)
            self.update_progress(0, "Error")
            messagebox.showerror("Error", error_msg)
        finally:
            # Re-enable the process button
            self.process_button.config(state='normal')


def main():
    root = tk.Tk()
    app = TimesheetProcessorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
