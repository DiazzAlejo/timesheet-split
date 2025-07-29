import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
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
        
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        # File selection section
        self.files_listbox = tk.Listbox(main_frame, height=4)
        self.files_listbox.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        ttk.Button(main_frame, text="Add PDF Files", command=self.add_pdf_files).grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        ttk.Button(main_frame, text="Clear Files", command=self.clear_files).grid(row=1, column=1, sticky=tk.W)
        ttk.Label(main_frame, text="Output Folder:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10))
        self.output_var = tk.StringVar()
        self.output_entry = ttk.Entry(main_frame, textvariable=self.output_var, state='readonly')
        self.output_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        ttk.Button(main_frame, text="Browse", command=self.select_output_folder).grid(row=2, column=2)
        self.process_button = ttk.Button(main_frame, text="Process PDFs", command=self.start_processing)
        self.process_button.grid(row=3, column=0, columnspan=3, pady=20)
        self.log_text = scrolledtext.ScrolledText(main_frame, height=8, state='disabled')
        self.log_text.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        
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
        self.process_button.config(state='disabled')
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')
        import threading
        thread = threading.Thread(target=self.process_pdfs)
        thread.daemon = True
        thread.start()
        
    def process_pdfs(self):
        try:
            self.log_message("Starting PDF processing...")
            options = {
                'ocr_enabled': True,
                'create_zip': True,
                'output_folder': self.output_folder,
                'progress_callback': self.update_progress,
                'log_callback': self.log_message
            }
            result = self.processor.process_pdfs(self.pdf_files, options)
            if result['success']:
                self.log_message(f"Processing completed successfully!")
                self.log_message(f"Output saved to: {result['output_path']}")
                files_created = result.get('files_created', 0)
                self.log_message(f"Total files created: {files_created}")
                self.update_progress(100, "Completed")
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
            self.process_button.config(state='normal')


def main():
    root = tk.Tk()
    app = TimesheetProcessorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
