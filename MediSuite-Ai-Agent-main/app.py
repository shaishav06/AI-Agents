import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from tkinter import ttk
import threading
import sys
import os
import re
from Agent import MedicalCodingAgent
from PIL import Image, ImageTk
import time
import subprocess
import platform
class MediSuiteGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MediSuite - Medical Coding Assistant")
        self.root.geometry("1100x750")  # Increased window size
        self.root.configure(bg="#f0f4f8")
        
        # Set app icon if available
        try:
            icon_path = "medisuite_icon.ico"
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass
            
        self.agent = MedicalCodingAgent()
        self.agent_output_lock = threading.Lock()
        self.conversation_thread = None
        self.user_input_ready = threading.Event()
        self.user_input_value = ""
        self.agent.current_state = "greeting"
        self.upload_enabled = False  # Track if upload is enabled
        self.pdf_preview_window = None  # For PDF preview window
        
        # Load images for buttons
        self.load_images()
        
        # Create UI elements
        self.create_widgets()
        
        # Start with greeting
        self.start_greeting()
        
        # Apply animations
        self.animate_startup()

    def load_images(self):
        # Create placeholder images if actual images aren't available
        self.send_icon = self.create_circle_image("#10b981", 20, "➤")
        self.upload_icon = self.create_circle_image("#2563eb", 20, "↑")
        self.reset_icon = self.create_circle_image("#f97316", 20, "↺")
        
    def create_circle_image(self, color, size, text):
        # Create a circular image with text
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(img)
        draw.ellipse((0, 0, size-1, size-1), fill=color)
        
        # Add text
        try:
            font = ImageFont.truetype("arial.ttf", size//2)
        except:
            font = ImageFont.load_default()
            
        # Fix for newer Pillow versions where textsize is deprecated
        try:
            # For newer Pillow versions
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except AttributeError:
            try:
                # For older Pillow versions
                text_width, text_height = draw.textsize(text, font=font)
            except:
                # Fallback if both methods fail
                text_width = size // 2
                text_height = size // 2
                
        position = ((size-text_width)//2, (size-text_height)//2)
        draw.text(position, text, fill="white", font=font)
        
        return ImageTk.PhotoImage(img)

    def create_widgets(self):
        # Configure custom styles
        self.configure_styles()
        
        # Main container with gradient background
        self.main_container = tk.Frame(self.root, bg="#f0f4f8")
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header with logo and title
        self.create_header()
        
        # Chat history with modern styling
        self.create_chat_area()
        
        # Input area with shadow effect
        self.create_input_area()
        
        # Status bar
        self.create_status_bar()

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Modern color palette
        primary_color = '#2563eb'    # Modern blue
        accent_color = '#10b981'     # Emerald green
        bg_color = '#f0f4f8'         # Light blue-gray
        entry_bg = '#ffffff'         # Pure white
        user_color = '#2563eb'       # Matching primary
        assistant_color = '#1e293b'  # Dark slate
        border_color = '#e2e8f0'     # Light border
        
        # Configure button styles
        style.configure('Rounded.TButton',
            font=('Segoe UI', 11, 'bold'),
            background=primary_color,
            foreground='white',
            borderwidth=0,
            focusthickness=3,
            focuscolor=accent_color,
            padding=(15, 10))
        
        style.map('Rounded.TButton',
            background=[('active', accent_color)],
            foreground=[('active', 'white')])
            
        # Secondary button style
        style.configure('Secondary.TButton',
            font=('Segoe UI', 11, 'bold'),
            background='#6366f1',
            foreground='white',
            borderwidth=0,
            focusthickness=3,
            focuscolor='#4f46e5',
            padding=(15, 10))
            
        style.map('Secondary.TButton',
            background=[('active', '#4f46e5')],
            foreground=[('active', 'white')])
        
        # Label style
        style.configure('TLabel',
            font=('Segoe UI', 11),
            background=bg_color)
        
        # Frame style
        style.configure('TFrame',
            background=bg_color)

    def create_header(self):
        # Header frame
        header_frame = tk.Frame(self.main_container, bg="#f0f4f8")
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        # App logo (placeholder)
        logo_text = "🏥"
        logo_label = tk.Label(header_frame, text=logo_text, font=('Segoe UI', 24), bg="#f0f4f8", fg="#2563eb")
        logo_label.pack(side=tk.LEFT)
        
        # App title
        title_label = tk.Label(header_frame, text="MediSuite", font=('Segoe UI', 18, 'bold'), bg="#f0f4f8", fg="#1e293b")
        title_label.pack(side=tk.LEFT, padx=10)
        
        subtitle_label = tk.Label(header_frame, text="Medical Coding Assistant", font=('Segoe UI', 12), bg="#f0f4f8", fg="#64748b")
        subtitle_label.pack(side=tk.LEFT)
        
        # Reset button on the right side of header
        self.reset_btn = tk.Button(
            header_frame,
            text="Reset Chat",
            font=('Segoe UI', 10, 'bold'),
            bg="#f97316",
            fg="white",
            activebackground="#ea580c",
            activeforeground="white",
            relief=tk.FLAT,
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2",
            command=self.reset_conversation
        )
        self.reset_btn.pack(side=tk.RIGHT)
        self.apply_button_hover_effect(self.reset_btn, "#f97316", "#ea580c")

    def create_chat_area(self):
        # Chat container with card-like appearance
        chat_container = tk.Frame(self.main_container, bg="#ffffff", bd=0, highlightthickness=1, highlightbackground="#e2e8f0")
        chat_container.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Add inner shadow effect
        shadow_frame = tk.Frame(chat_container, bg="#ffffff", bd=0)
        shadow_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Chat history with modern styling
        self.history = scrolledtext.ScrolledText(
            shadow_frame,
            wrap=tk.WORD,
            font=('Segoe UI', 11),
            bg="#ffffff",
            fg="#1e293b",
            height=20,
            state=tk.DISABLED,
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=15
        )
        self.history.pack(fill=tk.BOTH, expand=True)
        
        # Custom scrollbar styling
        self.history.vbar.configure(troughcolor="#f1f5f9", background="#94a3b8", activebackground="#64748b", width=12)

    def create_input_area(self):
        # Input container with shadow effect
        input_frame = tk.Frame(self.main_container, bg="#ffffff", bd=0, highlightthickness=1, highlightbackground="#e2e8f0")
        input_frame.pack(fill=tk.X, pady=(0, 10), ipady=5)
        
        # Inner padding frame
        input_container = tk.Frame(input_frame, bg="#ffffff", bd=0)
        input_container.pack(fill=tk.X, expand=True, padx=10, pady=5)
        
        # Input field with modern styling
        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(
            input_container,
            textvariable=self.input_var,
            font=('Segoe UI', 11),
            bg="#ffffff",
            fg="#1e293b",
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 10), ipady=10)
        self.input_entry.bind('<Return>', self.on_send)
        
        # Input placeholder text
        self.input_entry.insert(0, "Type your message here...")
        self.input_entry.config(fg="#94a3b8")
        
        # Add focus/unfocus events for placeholder
        self.input_entry.bind("<FocusIn>", self.on_entry_focus_in)
        self.input_entry.bind("<FocusOut>", self.on_entry_focus_out)
        
        # Button container
        button_container = tk.Frame(input_container, bg="#ffffff")
        button_container.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Modern buttons with hover effects
        self.send_btn = tk.Button(
            button_container,
            text="Send",
            font=('Segoe UI', 11, 'bold'),
            bg="#10b981",
            fg="white",
            activebackground="#059669",
            activeforeground="white",
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.on_send
        )
        self.send_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Add rounded corners to buttons using canvas
        self.apply_button_hover_effect(self.send_btn)
        
        self.upload_btn = tk.Button(
            button_container,
            text="Upload",
            font=('Segoe UI', 11, 'bold'),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.on_upload
        )
        self.upload_btn.pack(side=tk.LEFT)
        
        # Add hover effect
        self.apply_button_hover_effect(self.upload_btn)

    def create_status_bar(self):
        # Status bar at the bottom
        status_frame = tk.Frame(self.main_container, bg="#f0f4f8")
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Status indicator
        self.status_text = tk.Label(
            status_frame, 
            text="Ready", 
            font=('Segoe UI', 9),
            bg="#f0f4f8",
            fg="#64748b"
        )
        self.status_text.pack(side=tk.LEFT)
        
        # Version info
        version_text = tk.Label(
            status_frame, 
            text="v1.0.0", 
            font=('Segoe UI', 9),
            bg="#f0f4f8",
            fg="#94a3b8"
        )
        version_text.pack(side=tk.RIGHT)

    def apply_button_hover_effect(self, button, default_bg=None, hover_bg=None):
        def on_enter(e):
            if button["state"] != "disabled":
                if hover_bg:
                    button["bg"] = hover_bg
                else:
                    button["bg"] = "#059669" if button["text"] == "Send" else "#1d4ed8"
                
        def on_leave(e):
            if button["state"] != "disabled":
                if default_bg:
                    button["bg"] = default_bg
                else:
                    button["bg"] = "#10b981" if button["text"] == "Send" else "#2563eb"
                
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def on_entry_focus_in(self, event):
        if self.input_entry.get() == "Type your message here...":
            self.input_entry.delete(0, tk.END)
            self.input_entry.config(fg="#1e293b")

    def on_entry_focus_out(self, event):
        if not self.input_entry.get():
            self.input_entry.insert(0, "Type your message here...")
            self.input_entry.config(fg="#94a3b8")

    def animate_startup(self):
        # Simple fade-in effect for the main container
        self.main_container.update()
        
        # Start with transparent
        self.main_container.place_forget()
        
        # Gradually show the container
        def fade_in(alpha=0):
            if alpha < 1.0:
                alpha += 0.1
                # Simulate opacity with bg color
                self.root.update()
                self.root.after(50, lambda: fade_in(alpha))
            else:
                self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
                
        fade_in()

    def reset_conversation(self):
        # Ask for confirmation
        if messagebox.askyesno("Reset Conversation", "Are you sure you want to reset the conversation?"):
            # Clear chat history
            self.history.config(state=tk.NORMAL)
            self.history.delete(1.0, tk.END)
            self.history.config(state=tk.DISABLED)
            
            # Reset agent state
            self.agent = MedicalCodingAgent()
            self.agent.current_state = "greeting"
            
            # Reset conversation thread
            if self.conversation_thread and self.conversation_thread.is_alive():
                self.user_input_value = "exit"
                self.user_input_ready.set()
                self.conversation_thread.join(0.5)  # Wait a bit for thread to exit
                
            self.conversation_thread = None
            self.user_input_ready.clear()
            
            # Reset upload enabled flag
            self.upload_enabled = False
            
            # Update status
            self.status_text.config(text="Conversation reset")
            
            # Start new greeting
            self.start_greeting()
            
            # Show confirmation
            self.show_toast_notification("Conversation has been reset")

    def start_greeting(self):
        greeting = "Hello! I'm your AI medical coding assistant. I can help you code patient diagnoses and procedures, then generate insurance claims. Would you like to:\n\n1️⃣ Start with guided mode (I'll help you step by step)\n2️⃣ Use summary mode (provide all information at once)\n3️⃣ Upload a PDF/JPG document (I'll extract information from your document)"
        self.append_history("Assistant", greeting)

    def append_history(self, role, message):
        self.history.config(state=tk.NORMAL)
        
        if role == "User":
            # Add user message with bubble effect
            self.history.insert(tk.END, "\n", 'spacing')
            self.history.insert(tk.END, f"You: ", 'user_prefix')
            self.history.insert(tk.END, f"{message}\n", 'user_message')
        else:
            # Add assistant message with bubble effect
            self.history.insert(tk.END, "\n", 'spacing')
            self.history.insert(tk.END, f"🤖 Assistant: ", 'assistant_prefix')
            self.history.insert(tk.END, f"{message}\n", 'assistant_message')
            
        # Configure tags for styling
        self.history.tag_config('spacing', spacing1=5)
        self.history.tag_config('user_prefix', foreground='#2563eb', font=('Segoe UI', 11, 'bold'))
        self.history.tag_config('user_message', foreground='#1e293b', font=('Segoe UI', 11))
        self.history.tag_config('assistant_prefix', foreground='#10b981', font=('Segoe UI', 11, 'bold'))
        self.history.tag_config('assistant_message', foreground='#1e293b', font=('Segoe UI', 11))
        
        self.history.see(tk.END)
        self.history.config(state=tk.DISABLED)
        
        # Simulate typing effect for assistant messages
        if role == "Assistant":
            self.root.update()

    def on_send(self, event=None):
        user_input = self.input_var.get().strip()
        if not user_input or user_input == "Type your message here...":
            return
            
        # Check for option 3 selection to enable upload button
        if "3" in user_input and not self.upload_enabled:
            self.upload_enabled = True
            self.status_text.config(text="Upload enabled")
            
        # Disable buttons temporarily
        self.send_btn.config(state=tk.DISABLED)
        
        self.append_history("User", user_input)
        self.input_var.set("")
        self.user_input_value = user_input
        self.user_input_ready.set()
        
        if not self.conversation_thread or not self.conversation_thread.is_alive():
            self.conversation_thread = threading.Thread(target=self.conversation_loop, daemon=True)
            self.conversation_thread.start()
        
        # Re-enable buttons after a short delay
        self.root.after(500, lambda: self.send_btn.config(state=tk.NORMAL))

    def on_upload(self):
        if not self.upload_enabled:
            self.show_toast_notification("Please select option 3 first to enable document upload")
            return
            
        file_path = filedialog.askopenfilename(
            title="Select Medical Document",
            filetypes=[
                ("Document Files", "*.pdf *.jpg *.jpeg *.png"),
                ("PDF Files", "*.pdf"),
                ("Image Files", "*.jpg *.jpeg *.png")
            ]
        )
        
        if file_path:
            # Disable buttons temporarily
            self.send_btn.config(state=tk.DISABLED)
            
            self.append_history("User", f"[Uploaded file: {os.path.basename(file_path)}]")
            self.user_input_value = file_path
            self.user_input_ready.set()
            
            if not self.conversation_thread or not self.conversation_thread.is_alive():
                self.conversation_thread = threading.Thread(target=self.conversation_loop, daemon=True)
                self.conversation_thread.start()
            
            # Re-enable buttons after a short delay
            self.root.after(500, lambda: self.send_btn.config(state=tk.NORMAL))

    def show_toast_notification(self, message):
        """Show a temporary toast notification"""
        # Create a toast frame
        toast_frame = tk.Frame(self.root, bg="#1e293b", bd=0)
        toast_frame.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
        
        # Add message
        toast_label = tk.Label(
            toast_frame,
            text=message,
            font=('Segoe UI', 11),
            bg="#1e293b",
            fg="white",
            padx=15,
            pady=10
        )
        toast_label.pack()
        
        # Auto-dismiss after 3 seconds
        self.root.after(3000, toast_frame.destroy)

    def conversation_loop(self):
        while True:
            self.user_input_ready.wait()
            user_input = self.user_input_value
            self.user_input_ready.clear()
            
            if user_input.lower() in ["exit", "quit", "bye"]:
                self.append_history("Assistant", "Thank you for using the Medical Coding Assistant. Goodbye!")
                break
                
            self.agent.add_to_history("user", user_input)
            try:
                if self.agent.current_state == "collecting_patient_info":
                    self.collect_patient_info_gui(user_input)
                elif self.agent.current_state == "collecting_clinical_notes":
                    self.collect_clinical_notes_gui(user_input)
                elif self.agent.current_state == "confirming_codes":
                    self.confirm_codes_gui(user_input)
                elif self.agent.current_state == "reviewing_claim":
                    self.review_claim_gui(user_input)
                elif self.agent.current_state == "post_claim_menu":
                    self.handle_post_claim_menu_gui(user_input)
                elif self.agent.current_state == "collecting_summary":
                    self.collect_summary_gui(user_input)
                elif self.agent.current_state == "code_lookup":
                    self.code_lookup_gui(user_input)
                elif self.agent.current_state == "processing_document":
                    self.process_document_gui(user_input)
                else:
                    self.handle_default_conversation_gui(user_input)
            except Exception as e:
                self.append_history("Assistant", f"Sorry, I encountered an error: {str(e)}")

    # GUI wrappers for agent methods
    def collect_patient_info_gui(self, user_input):
        old_stdout = sys.stdout
        sys.stdout = self
        self.agent.collect_patient_info(user_input)
        sys.stdout = old_stdout

    def collect_clinical_notes_gui(self, user_input):
        old_stdout = sys.stdout
        sys.stdout = self
        self.agent.collect_clinical_notes(user_input)
        sys.stdout = old_stdout

    def confirm_codes_gui(self, user_input):
        old_stdout = sys.stdout
        sys.stdout = self
        self.agent.confirm_codes(user_input)
        sys.stdout = old_stdout

    def review_claim_gui(self, user_input):
        old_stdout = sys.stdout
        sys.stdout = self
        self.agent.review_claim(user_input)
        sys.stdout = old_stdout

    def handle_post_claim_menu_gui(self, user_input):
        old_stdout = sys.stdout
        sys.stdout = self
        self.agent.handle_post_claim_menu(user_input)
        
        # Check if a PDF was generated and offer to preview it
        if "claim" in user_input.lower() and any(word in user_input.lower() for word in ["generate", "create", "show", "view", "preview"]):
            # Look for generated PDF files in the current directory
            pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf') and 'claim' in f.lower()]
            if pdf_files:
                # Sort by creation time, newest first
                pdf_files.sort(key=lambda x: os.path.getctime(x), reverse=True)
                newest_pdf = pdf_files[0]
                
                # Ask if user wants to preview the PDF
                self.show_pdf_preview_button(newest_pdf)
        
        sys.stdout = old_stdout

    def show_pdf_preview_button(self, pdf_path):
        """Show a button to preview the PDF"""
        # Create a frame for the preview button
        preview_frame = tk.Frame(self.main_container, bg="#f0f4f8", pady=10)
        preview_frame.pack(fill=tk.X)
        
        # Add a label
        preview_label = tk.Label(
            preview_frame,
            text="PDF claim form generated!",
            font=('Segoe UI', 12, 'bold'),
            bg="#f0f4f8",
            fg="#1e293b"
        )
        preview_label.pack(side=tk.LEFT, padx=10)
        
        # Add open with default viewer button
        open_btn = tk.Button(
            preview_frame,
            text="View PDF",
            font=('Segoe UI', 11, 'bold'),
            bg="#6366f1",  # Indigo
            fg="white",
            activebackground="#4f46e5",
            activeforeground="white",
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            command=lambda: self.open_with_default_app(pdf_path)
        )
        open_btn.pack(side=tk.LEFT, padx=5)
        
        # Add hover effect
        self.apply_button_hover_effect(open_btn, "#6366f1", "#4f46e5")
    
    def open_with_default_app(self, file_path):
        """Open a file with the default system application"""
        try:
            if platform.system() == 'Darwin':  # macOS
                subprocess.call(('open', file_path))
            elif platform.system() == 'Windows':  # Windows
                os.startfile(file_path)
            else:  # Linux
                subprocess.call(('xdg-open', file_path))
                
            self.show_toast_notification(f"Opening {os.path.basename(file_path)} with default viewer")
        except Exception as e:
            self.show_toast_notification(f"Error opening file: {str(e)}")

    def collect_summary_gui(self, user_input):
        old_stdout = sys.stdout
        sys.stdout = self
        self.agent.collect_summary(user_input)
        sys.stdout = old_stdout

    def code_lookup_gui(self, user_input):
        old_stdout = sys.stdout
        sys.stdout = self
        self.agent.code_lookup(user_input)
        sys.stdout = old_stdout

    def process_document_gui(self, user_input):
        old_stdout = sys.stdout
        sys.stdout = self
        self.agent.process_document(user_input)
        sys.stdout = old_stdout

    def handle_default_conversation_gui(self, user_input):
        old_stdout = sys.stdout
        sys.stdout = self
        
        # Check for option 3 selection in default conversation handler
        if "3" in user_input and any(keyword in user_input.lower() for keyword in ["option", "upload", "document", "pdf", "jpg", "image"]):
            self.upload_enabled = True
            self.status_text.config(text="Upload enabled")
            
        self.agent.handle_default_conversation(user_input)
        sys.stdout = old_stdout

    # Redirect print to GUI
    def write(self, message):
        if message.strip():
            self.append_history("Assistant", message.strip())
    def flush(self):
        pass

def main():
    root = tk.Tk()
    # Set window minimum size
    root.minsize(900, 600)
    
    # Center window on screen
    window_width = 1100
    window_height = 750
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    app = MediSuiteGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()