import os
import threading
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
from PIL import Image
import pywinstyles
import ctypes

try:
    myappid = 'pixelflow.studio.resizer.1'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

# --- Modern Theme Configuration ---
ctk.set_appearance_mode("Dark")
BG_COLOR = "#18181b"          # Deep background
CARD_COLOR = "#27272a"        # Slightly lighter elevated card
ACCENT_COLOR = "#3b82f6"      # Modern soft blue
ACCENT_HOVER = "#2563eb"      # Darker blue for hover
DANGER_COLOR = "#ef4444"      # Soft red for warnings/close
TEXT_PRIMARY = "#f4f4f5"
TEXT_SECONDARY = "#a1a1aa"

class PixelFlowApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- WINDOW SETUP ---
        self.title("PixelFlow Studio")
        self.geometry("850x900")
        self.minsize(800, 750)
        self.configure(fg_color=BG_COLOR)
        
        try:
            pywinstyles.apply_style(self, "mica")
            pywinstyles.change_header_color(self, color=BG_COLOR)
        except Exception:
            pass
        
        # --- LOGO SETUP ---
        self.iconbitmap("icon.ico") 

        self._build_main_ui()

    def _build_main_ui(self):
        self.main_content = ctk.CTkFrame(self, corner_radius=0, fg_color=BG_COLOR)
        self.main_content.pack(fill="both", expand=True, padx=30, pady=10)

        # --- MAIN SETTINGS CARD ---
        self.settings_card = ctk.CTkFrame(self.main_content, corner_radius=12, fg_color=CARD_COLOR, border_width=1, border_color="#3f3f46")
        self.settings_card.pack(fill="x", pady=(0, 20))

        # 1. Directory Selection
        self.dir_frame = ctk.CTkFrame(self.settings_card, fg_color="transparent")
        self.dir_frame.pack(fill="x", padx=25, pady=25)
        
        self.folder_path = tk.StringVar()
        self.btn_browse = ctk.CTkButton(self.dir_frame, text="Select Image Folder", command=self.browse_folder, height=40, width=200, fg_color="#3f3f46", hover_color="#52525b", font=("Segoe UI", 13), corner_radius=6)
        self.btn_browse.pack(side="left")
        
        self.lbl_folder = ctk.CTkLabel(self.dir_frame, textvariable=self.folder_path, text="No folder selected", text_color=TEXT_SECONDARY, font=("Segoe UI", 12))
        self.lbl_folder.pack(side="left", padx=15)

        # Separator
        ctk.CTkFrame(self.settings_card, height=1, fg_color="#3f3f46").pack(fill="x", padx=25)

        # 2. Resizing Rules Grid
        self.rules_frame = ctk.CTkFrame(self.settings_card, fg_color="transparent")
        self.rules_frame.pack(fill="x", padx=25, pady=20)
        self.rules_frame.columnconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkLabel(self.rules_frame, text="Resize Dimensions", font=("Segoe UI Semibold", 15), text_color=TEXT_PRIMARY).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 15))

        # Landscape
        ctk.CTkLabel(self.rules_frame, text="Landscape Output (W × H)", text_color=TEXT_PRIMARY, font=("Segoe UI", 13)).grid(row=1, column=0, sticky="w", pady=5)
        self.entry_w_a = self._create_input(self.rules_frame, "1920")
        self.entry_w_a.grid(row=1, column=1, sticky="e")
        ctk.CTkLabel(self.rules_frame, text="×", text_color=TEXT_SECONDARY).grid(row=1, column=2)
        self.entry_h_a = self._create_input(self.rules_frame, "1080")
        self.entry_h_a.grid(row=1, column=3, sticky="w")

        # Portrait
        ctk.CTkLabel(self.rules_frame, text="Portrait Output (W × H)", text_color=TEXT_PRIMARY, font=("Segoe UI", 13)).grid(row=2, column=0, sticky="w", pady=5)
        self.entry_w_b = self._create_input(self.rules_frame, "1080")
        self.entry_w_b.grid(row=2, column=1, sticky="e")
        ctk.CTkLabel(self.rules_frame, text="×", text_color=TEXT_SECONDARY).grid(row=2, column=2)
        self.entry_h_b = self._create_input(self.rules_frame, "1920")
        self.entry_h_b.grid(row=2, column=3, sticky="w")

        # Oversize Exception
        ctk.CTkLabel(self.rules_frame, text="Oversize Protection", font=("Segoe UI Semibold", 13), text_color=ACCENT_COLOR).grid(row=3, column=0, columnspan=4, sticky="w", pady=(20, 5))
        
        limit_frame = ctk.CTkFrame(self.rules_frame, fg_color="transparent")
        limit_frame.grid(row=4, column=0, columnspan=4, sticky="w")
        
        ctk.CTkLabel(limit_frame, text="If width exceeds:", text_color=TEXT_SECONDARY, font=("Segoe UI", 12)).pack(side="left")
        self.entry_limit_w = self._create_input(limit_frame, "3000", width=70)
        self.entry_limit_w.pack(side="left", padx=10)
        
        ctk.CTkLabel(limit_frame, text="px, forcefully scale to:", text_color=TEXT_SECONDARY, font=("Segoe UI", 12)).pack(side="left", padx=(0, 10))
        self.entry_w_c = self._create_input(limit_frame, "2500")
        self.entry_w_c.pack(side="left")
        ctk.CTkLabel(limit_frame, text=" × ", text_color=TEXT_SECONDARY).pack(side="left", padx=5)
        self.entry_h_c = self._create_input(limit_frame, "1406")
        self.entry_h_c.pack(side="left")

        # 3. Actions & Execution
        self.action_frame = ctk.CTkFrame(self.settings_card, fg_color="transparent")
        self.action_frame.pack(fill="x", padx=25, pady=(0, 25))

        self.overwrite_var = ctk.BooleanVar(value=False)
        self.switch_overwrite = ctk.CTkSwitch(
            self.action_frame, text="Overwrite original images (Caution)",
            font=("Segoe UI", 12), text_color=TEXT_SECONDARY,
            variable=self.overwrite_var, onvalue=True, offvalue=False,
            progress_color=DANGER_COLOR, switch_width=40, switch_height=20
        )
        self.switch_overwrite.pack(side="left")

        self.btn_run = ctk.CTkButton(
            self.action_frame, text="Start Resizing",
            command=self.start_thread, width=160, height=40,
            fg_color=ACCENT_COLOR, text_color="#ffffff", hover_color=ACCENT_HOVER,
            font=("Segoe UI Semibold", 14), corner_radius=6
        )
        self.btn_run.pack(side="right")

        self.progress = ctk.CTkProgressBar(self.settings_card, height=3, mode="determinate", progress_color=ACCENT_COLOR, fg_color="#3f3f46")

        # --- HISTORY AREA ---
        self.history_label = ctk.CTkLabel(self.main_content, text="Job History", font=("Segoe UI Semibold", 14), text_color=TEXT_PRIMARY)
        self.history_label.pack(anchor="w", pady=(10, 5))
        
        self.history_scroll = ctk.CTkScrollableFrame(self.main_content, fg_color=CARD_COLOR, corner_radius=12, border_width=1, border_color="#3f3f46")
        self.history_scroll.pack(fill="both", expand=True)

    def _create_input(self, parent, default_val, width=80):
        entry = ctk.CTkEntry(parent, width=width, height=32, fg_color="#18181b", border_color="#3f3f46", text_color=TEXT_PRIMARY, corner_radius=6)
        entry.insert(0, default_val)
        return entry

    # --- App Logic ---
    def browse_folder(self):
        folder = tk.filedialog.askdirectory()
        if folder: self.folder_path.set(folder)

    def start_thread(self):
        if not self.folder_path.get(): return
        self.btn_run.configure(state="disabled", text="Processing...")
        self.progress.set(0)
        self.progress.pack(fill="x", side="bottom")
        threading.Thread(target=self.process_images, daemon=True).start()

    def add_history_item(self, img_orig, img_new, filename, logic_used):
        preview_height = 50
        def create_thumb(pil_img):
            aspect = pil_img.width / pil_img.height
            new_w = int(preview_height * aspect)
            thumb = pil_img.copy()
            thumb.thumbnail((new_w, preview_height))
            return ctk.CTkImage(light_image=thumb, dark_image=thumb, size=(new_w, preview_height))
        try:
            ctk_orig = create_thumb(img_orig)
            ctk_new = create_thumb(img_new)
            self.after(0, lambda: self._ui_add_row(ctk_orig, ctk_new, filename, logic_used))
        except Exception as e: print(f"Thumbnail error: {e}")

    def _ui_add_row(self, img_o, img_n, fname, logic_used):
        row = ctk.CTkFrame(self.history_scroll, fg_color=BG_COLOR, corner_radius=6)
        row.pack(fill="x", pady=4, padx=5)
        
        ctk.CTkLabel(row, text="", image=img_o).pack(side="left", padx=10, pady=5)
        ctk.CTkLabel(row, text="→", text_color=TEXT_SECONDARY, font=("Arial", 16)).pack(side="left", padx=5)
        ctk.CTkLabel(row, text="", image=img_n).pack(side="left", padx=10, pady=5)
        
        info_frame = ctk.CTkFrame(row, fg_color="transparent")
        info_frame.pack(side="left", padx=10, fill="y", pady=5)
        ctk.CTkLabel(info_frame, text=fname, text_color=TEXT_PRIMARY, font=("Segoe UI", 12)).pack(anchor="w")
        ctk.CTkLabel(info_frame, text=logic_used, text_color=TEXT_SECONDARY, font=("Segoe UI", 11)).pack(anchor="w")
        
        ctk.CTkLabel(row, text="Success", text_color="#10b981", font=("Segoe UI Semibold", 11)).pack(side="right", padx=15)

    def reset_ui(self):
        self.btn_run.configure(state="normal", text="Start Resizing")
        self.progress.pack_forget()

    def process_images(self):
        directory = self.folder_path.get()
        try:
            w_a, h_a = int(self.entry_w_a.get()), int(self.entry_h_a.get())
            w_b, h_b = int(self.entry_w_b.get()), int(self.entry_h_b.get())
            limit_w, w_c, h_c = int(self.entry_limit_w.get()), int(self.entry_w_c.get()), int(self.entry_h_c.get())
        except ValueError:
            self.after(0, self.reset_ui)
            return

        overwrite = self.overwrite_var.get()
        supported = ('.png', '.jpg', '.jpeg', '.bmp', '.webp', '.tiff')
        
        all_files = []
        for root, _, files in os.walk(directory):
            for f in files:
                if f.lower().endswith(supported):
                    if not overwrite and "-resized" in f: continue
                    all_files.append(os.path.join(root, f))
        
        total = len(all_files)
        if total == 0:
            self.after(0, self.reset_ui)
            return

        for i, file_path in enumerate(all_files):
            try:
                self.progress.set((i + 1) / total)
                
                with Image.open(file_path) as img:
                    preview_orig = img.copy()
                    width, height = img.size
                    
                    if width > limit_w:
                        t_w, t_h, logic = w_c, h_c, "Oversize Limit Applied"
                    elif width > height:
                        t_w, t_h, logic = w_a, h_a, "Landscape Scale"
                    else:
                        t_w, t_h, logic = w_b, h_b, "Portrait Scale"

                    ratio = min(t_w / width, t_h / height)
                    new_w, new_h = int(width * ratio), int(height * ratio)

                    final_img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                    if file_path.lower().endswith(('.jpg', '.jpeg')) and final_img.mode in ('RGBA', 'P'):
                        final_img = final_img.convert('RGB')

                    save_path = file_path if overwrite else f"{os.path.splitext(file_path)[0]}-resized{os.path.splitext(file_path)[1]}"

                    self.add_history_item(preview_orig, final_img, os.path.basename(save_path), logic)
                    final_img.save(save_path, quality=90, optimize=True)
                            
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

        self.after(0, self.reset_ui)

if __name__ == "__main__":
    app = PixelFlowApp()
    app.mainloop()