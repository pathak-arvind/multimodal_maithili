import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import pytesseract
import os
from ocr import extract_text_from_image
from transliteration import text_transliterate
from code_mixed import process_mixed_corpus
from stt import audio
from translate import translate_maithili_to_english 

class TranslationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maithili Translation System")
        self.root.geometry("900x700")
        
        # Initialize variables
        self.current_input_mode = "Text"
        self.selected_file_path = None
        
        # Set theme and colors
        self.style = ttk.Style()
        self.primary_color = "#3498db"
        self.secondary_color = "#2ecc71"
        self.bg_color = "#f5f5f5"
        
        # Configure main window
        self.root.configure(bg=self.bg_color)
        self.create_widgets()
        
    def create_widgets(self):
        # Create main frame
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_label = ttk.Label(main_frame, text="Maithili Translation System", font=("Arial", 16, "bold"))
        header_label.pack(pady=(0, 15))
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Input", padding=10)
        input_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Input method selection
        input_method_frame = ttk.Frame(input_frame)
        input_method_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(input_method_frame, text="Select Input Method:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.input_mode_var = tk.StringVar(value="Text")
        
        text_rb = ttk.Radiobutton(input_method_frame, text="Text", value="Text", 
                               variable=self.input_mode_var, command=self.change_input_mode)
        text_rb.pack(side=tk.LEFT, padx=5)
        
        speech_rb = ttk.Radiobutton(input_method_frame, text="Speech", value="Speech", 
                                 variable=self.input_mode_var, command=self.change_input_mode)
        speech_rb.pack(side=tk.LEFT, padx=5)
        
        image_rb = ttk.Radiobutton(input_method_frame, text="Image", value="Image", 
                                variable=self.input_mode_var, command=self.change_input_mode)
        image_rb.pack(side=tk.LEFT, padx=5)
        
        # Input content area
        self.input_content_frame = ttk.Frame(input_frame)
        self.input_content_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Text input (default)
        self.text_input_frame = ttk.Frame(self.input_content_frame)
        self.text_input_frame.pack(fill=tk.BOTH, expand=True)
        
        self.input_text = scrolledtext.ScrolledText(self.text_input_frame, height=8, wrap=tk.WORD)
        self.input_text.pack(fill=tk.BOTH, expand=True)
        self.input_text.insert("1.0", "Enter Maithili text here...")
        
        # File input (initially hidden)
        self.file_input_frame = ttk.Frame(self.input_content_frame)
        
        file_button_frame = ttk.Frame(self.file_input_frame)
        file_button_frame.pack(fill=tk.X, pady=10)
        
        self.file_path_var = tk.StringVar()
        self.file_label = ttk.Label(file_button_frame, textvariable=self.file_path_var, width=40)
        self.file_label.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        self.browse_button = ttk.Button(file_button_frame, text="Browse", command=self.browse_file)
        self.browse_button.pack(side=tk.RIGHT)
        
        # Preview frame
        self.preview_frame = ttk.Frame(self.file_input_frame)
        self.preview_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.preview_label = ttk.Label(self.preview_frame, text="File preview will appear here")
        self.preview_label.pack(pady=10)
        
        # Processing options
        options_frame = ttk.Frame(input_frame)
        options_frame.pack(fill=tk.X, pady=10)
        
        self.transliterate_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Transliterate", variable=self.transliterate_var).pack(side=tk.LEFT, padx=5)
        
        self.code_mix_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Detect Code-Mix", variable=self.code_mix_var).pack(side=tk.LEFT, padx=5)
        
        self.translate_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Translate", variable=self.translate_var).pack(side=tk.LEFT, padx=5)
        
        self.clean_english_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Clean English", variable=self.clean_english_var).pack(side=tk.LEFT, padx=5)
        
        # Process button
        process_frame = ttk.Frame(input_frame)
        process_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(process_frame, text="Clear", command=self.clear_input).pack(side=tk.LEFT)
        
        process_button = ttk.Button(process_frame, text="Process", command=self.process_input)
        process_button.pack(side=tk.RIGHT)
        
        # Output section
        output_frame = ttk.LabelFrame(main_frame, text="Output", padding=10)
        output_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create notebook for output tabs
        self.output_notebook = ttk.Notebook(output_frame)
        self.output_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs for each processing stage
        self.raw_tab = ttk.Frame(self.output_notebook)
        self.transliteration_tab = ttk.Frame(self.output_notebook)
        self.code_mix_tab = ttk.Frame(self.output_notebook)
        self.translation_tab = ttk.Frame(self.output_notebook)
        self.clean_english_tab = ttk.Frame(self.output_notebook)
        
        self.output_notebook.add(self.raw_tab, text="Raw Input")
        self.output_notebook.add(self.transliteration_tab, text="Transliteration")
        self.output_notebook.add(self.code_mix_tab, text="Code-Mix")
        self.output_notebook.add(self.translation_tab, text="Translation")
        self.output_notebook.add(self.clean_english_tab, text="Clean English")
        
        # Create text widgets for each tab
        self.raw_output = scrolledtext.ScrolledText(self.raw_tab, height=8, wrap=tk.WORD)
        self.raw_output.pack(fill=tk.BOTH, expand=True)
        
        self.transliteration_output = scrolledtext.ScrolledText(self.transliteration_tab, height=8, wrap=tk.WORD)
        self.transliteration_output.pack(fill=tk.BOTH, expand=True)
        
        self.code_mix_output = scrolledtext.ScrolledText(self.code_mix_tab, height=8, wrap=tk.WORD)
        self.code_mix_output.pack(fill=tk.BOTH, expand=True)
        
        self.translation_output = scrolledtext.ScrolledText(self.translation_tab, height=8, wrap=tk.WORD)
        self.translation_output.pack(fill=tk.BOTH, expand=True)
        
        self.clean_english_output = scrolledtext.ScrolledText(self.clean_english_tab, height=8, wrap=tk.WORD)
        self.clean_english_output.pack(fill=tk.BOTH, expand=True)
        
        # Output buttons
        output_buttons_frame = ttk.Frame(output_frame)
        output_buttons_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(output_buttons_frame, text="Copy", command=self.copy_output).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(output_buttons_frame, text="Save", command=self.save_output).pack(side=tk.LEFT, padx=5)
        ttk.Button(output_buttons_frame, text="Clear", command=self.clear_output).pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def change_input_mode(self):
        """Change the input mode based on selection"""
        mode = self.input_mode_var.get()
        
        # Hide both frames
        self.text_input_frame.pack_forget()
        self.file_input_frame.pack_forget()
        
        # Show appropriate frame
        if mode == "Text":
            self.text_input_frame.pack(fill=tk.BOTH, expand=True)
            self.browse_button.config(text="Browse")
        elif mode == "Speech":
            self.file_input_frame.pack(fill=tk.BOTH, expand=True)
            self.browse_button.config(text="Browse Audio")
        elif mode == "Image":
            self.file_input_frame.pack(fill=tk.BOTH, expand=True)
            self.browse_button.config(text="Browse Image")
            
        self.current_input_mode = mode
        self.status_var.set(f"Input mode changed to {mode}")
        
    def browse_file(self):
        """Browse for a file based on current input mode"""
        mode = self.current_input_mode
        
        if mode == "Speech":
            filetypes = [("Audio Files", "*.wav *.mp3 *.ogg")]
        elif mode == "Image":
            filetypes = [("Image Files", "*.jpg *.jpeg *.png *.bmp")]
        else:
            return
            
        file_path = filedialog.askopenfilename(filetypes=filetypes)
        if file_path:
            self.selected_file_path = file_path
            self.file_path_var.set(os.path.basename(file_path))
            self.status_var.set(f"Selected file: {os.path.basename(file_path)}")
            
            # Show preview if it's an image
            if mode == "Image":
                self.show_image_preview(file_path)
            elif mode == "Speech":
                self.show_audio_preview(file_path)
                
    def show_image_preview(self, file_path):
        """Show preview of selected image"""
        # Clear previous preview
        for widget in self.preview_frame.winfo_children():
            widget.destroy()
            
        try:
            # Open image
            image = Image.open(file_path)
            
            # Resize for preview
            width, height = image.size
            max_size = 300
            if width > max_size or height > max_size:
                ratio = min(max_size/width, max_size/height)
                new_size = (int(width * ratio), int(height * ratio))
                image = image.resize(new_size, Image.LANCZOS)
                
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(image)
            
            # Display image
            img_label = ttk.Label(self.preview_frame, image=photo)
            img_label.image = photo  # Keep a reference
            img_label.pack(padx=10, pady=10)
            
        except Exception as e:
            error_label = ttk.Label(self.preview_frame, text=f"Error loading image: {str(e)}")
            error_label.pack(padx=10, pady=10)
            
    def show_audio_preview(self, file_path):
        """Show info about selected audio file"""
        # Clear previous preview
        for widget in self.preview_frame.winfo_children():
            widget.destroy()
            
        # Show audio file info
        info_text = f"Audio File: {os.path.basename(file_path)}\n"
        info_text += f"Size: {os.path.getsize(file_path) / 1024:.1f} KB\n"
        info_text += "Click 'Process' to transcribe audio"
        
        info_label = ttk.Label(self.preview_frame, text=info_text)
        info_label.pack(padx=10, pady=10)
            
    def clear_input(self):
        """Clear all input fields"""
        if self.current_input_mode == "Text":
            self.input_text.delete("1.0", tk.END)
        else:
            self.file_path_var.set("")
            self.selected_file_path = None
            # Clear preview
            for widget in self.preview_frame.winfo_children():
                widget.destroy()
            self.preview_label = ttk.Label(self.preview_frame, text="File preview will appear here")
            self.preview_label.pack(pady=10)
            
        self.status_var.set("Input cleared")
        
    def process_input(self):
        """Process the input based on current mode and options"""
        mode = self.current_input_mode
        
        # Get the input text based on mode
        if mode == "Text":
            input_text = self.input_text.get("1.0", tk.END).strip()
            if not input_text:
                messagebox.showwarning("Empty Input", "Please enter some text to process.")
                return
        elif mode in ["Speech", "Image"]:
            if not self.selected_file_path:
                messagebox.showwarning("No File", f"Please select a file for {mode} input.")
                return
                
            # Mock extraction based on mode
            if mode == "Speech":
                input_text = audio(self.selected_file_path)
            else:  # Image
                try:
                    input_text = extract_text_from_image(self.selected_file_path)
                except Exception as e:
                    messagebox.showerror("OCR Error", f"Error processing image: {str(e)}")
                    return
                    
        # Display raw input
        self.raw_output.delete("1.0", tk.END)
        self.raw_output.insert("1.0", input_text)
        
        # Process based on selected options
        if self.transliterate_var.get():
            transliterated = text_transliterate(input_text)
            self.transliteration_output.delete("1.0", tk.END)
            self.transliteration_output.insert("1.0", transliterated)
            
        if self.code_mix_var.get():
            code_mixed = process_mixed_corpus(input_text)
            self.code_mix_output.delete("1.0", tk.END)
            self.code_mix_output.insert("1.0", code_mixed)
            
        if self.translate_var.get():
            translated = translate_maithili_to_english(input_text)
            self.translation_output.delete("1.0", tk.END)
            self.translation_output.insert("1.0", translated)
            
        if self.clean_english_var.get():
            clean_english = translate_maithili_to_english(input_text)
            self.clean_english_output.delete("1.0", tk.END)
            self.clean_english_output.insert("1.0", clean_english)
            
        # Switch to output tab
        self.output_notebook.select(0)  # Show raw output first
        
        self.status_var.set("Processing complete")
        
    def clear_output(self):
        """Clear all output fields"""
        self.raw_output.delete("1.0", tk.END)
        self.transliteration_output.delete("1.0", tk.END)
        self.code_mix_output.delete("1.0", tk.END)
        self.translation_output.delete("1.0", tk.END)
        self.clean_english_output.delete("1.0", tk.END)
        
        self.status_var.set("Output cleared")
        
    def copy_output(self):
        """Copy current tab's output to clipboard"""
        selected_tab = self.output_notebook.index(self.output_notebook.select())
        
        if selected_tab == 0:
            text = self.raw_output.get("1.0", tk.END).strip()
        elif selected_tab == 1:
            text = self.transliteration_output.get("1.0", tk.END).strip()
        elif selected_tab == 2:
            text = self.code_mix_output.get("1.0", tk.END).strip()
        elif selected_tab == 3:
            text = self.translation_output.get("1.0", tk.END).strip()
        elif selected_tab == 4:
            text = self.clean_english_output.get("1.0", tk.END).strip()
        else:
            return
            
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.status_var.set("Copied to clipboard")
        
    def save_output(self):
        """Save current tab's output to file"""
        selected_tab = self.output_notebook.index(self.output_notebook.select())
        tab_names = ["Raw", "Transliteration", "CodeMix", "Translation", "CleanEnglish"]
        
        if selected_tab == 0:
            text = self.raw_output.get("1.0", tk.END).strip()
        elif selected_tab == 1:
            text = self.transliteration_output.get("1.0", tk.END).strip()
        elif selected_tab == 2:
            text = self.code_mix_output.get("1.0", tk.END).strip()
        elif selected_tab == 3:
            text = self.translation_output.get("1.0", tk.END).strip()
        elif selected_tab == 4:
            text = self.clean_english_output.get("1.0", tk.END).strip()
        else:
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"maithili_{tab_names[selected_tab]}.txt"
        )
        
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text)
            self.status_var.set(f"Saved to {os.path.basename(file_path)}")

# Import these dummy functions from your original code
def whisper_stt(audio_file):
    return "Transcribed text from speech"

def ocr_image(image_path):
    return pytesseract.image_to_string(Image.open(image_path))

def transliterate(text):
    return f"Transliterated: {text}"

def detect_code_mix(text):
    return f"Code-Mixed Segments: {text}"

def translate(text):
    return f"Translated to English: {text}"

def convert_to_clean_english(text):
    return f"Clean English: {text}"

# Main function
if __name__ == "__main__":
    root = tk.Tk()
    app = TranslationApp(root)
    root.mainloop()