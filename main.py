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
        
        # Configure style for a modern look
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#f7f7fa')
        style.configure('TButton', font=('Segoe UI', 10, 'bold'), padding=6)
        style.configure('TLabel', background='#f7f7fa', font=('Segoe UI', 10))
        style.configure('Header.TLabel', background='#f7f7fa', font=('Segoe UI', 14, 'bold'))
        style.configure('TEntry', font=('Segoe UI', 10))
        
        self.pdf_files = []
        # Set default output folder to Downloads
        self.output_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
        self.processor = PDFProcessor()
        self.progress_var = tk.DoubleVar(value=0)
        self.status_var = tk.StringVar(value="Ready")
        self.setup_ui()
        
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="18")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Header
        header = ttk.Label(main_frame, text="Timesheet PDF Processor", style='Header.TLabel')
        header.grid(row=0, column=0, columnspan=3, pady=(0, 18))

        # File selection section
        files_label = ttk.Label(main_frame, text="Selected PDF Files:")
        files_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 4))
        self.files_listbox = tk.Listbox(main_frame, height=6, font=('Segoe UI', 10), bg='#fff', relief='groove', borderwidth=2)
        self.files_listbox.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))

        add_btn = ttk.Button(main_frame, text="Add PDF Files", command=self.add_pdf_files)
        add_btn.grid(row=3, column=0, sticky=tk.W, padx=(0, 5), pady=(0, 10))
        clear_btn = ttk.Button(main_frame, text="Clear Files", command=self.clear_files)
        clear_btn.grid(row=3, column=1, sticky=tk.W, pady=(0, 10))

        # Output folder section
        out_label = ttk.Label(main_frame, text="Output Folder:")
        out_label.grid(row=4, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.output_var = tk.StringVar()
        self.output_entry = ttk.Entry(main_frame, textvariable=self.output_var, state='readonly', width=40)
        self.output_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), padx=(0, 10), pady=(10, 0))
        browse_btn = ttk.Button(main_frame, text="Browse", command=self.select_output_folder)
        browse_btn.grid(row=4, column=2, pady=(10, 0))

        # Progress bar
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100, length=300)
        self.progress_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))

        # Process button
        self.process_button = ttk.Button(main_frame, text="Process PDFs", command=self.start_processing)
        self.process_button.grid(row=6, column=0, columnspan=3, pady=24, sticky=(tk.W, tk.E))

        # Log section
        log_label = ttk.Label(main_frame, text="Processing Log:")
        log_label.grid(row=7, column=0, sticky=tk.W, pady=(10, 4))
        self.log_text = scrolledtext.ScrolledText(main_frame, height=10, font=('Consolas', 10), bg='#f9f9f9', relief='groove', borderwidth=2, state='disabled')
        self.log_text.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

        # Make resizing smooth
        for i in range(9):
            main_frame.rowconfigure(i, weight=0)
        main_frame.rowconfigure(8, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)
        
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
