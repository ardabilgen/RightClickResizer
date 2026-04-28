import sys
import os
import tkinter as tk
from tkinter import messagebox, Scrollbar
from config import load_config, save_config
from resizer import resize_image
from video_converter import convert_to_mp4, VIDEO_EXTENSIONS
from context_menu import install_context_menu, uninstall_context_menu, is_admin
import ctypes


def is_video_file(file_path):
    """Check if a file is a video based on extension."""
    _, ext = os.path.splitext(file_path)
    return ext.lower() in VIDEO_EXTENSIONS


def run_gui():
    print("Starting GUI...")
    
    root = tk.Tk()
    root.title("RightClickResizer - Image & Video Tool")
    root.geometry("500x600")
    root.minsize(400, 400)
    
    config = load_config()
    
    # Main scrollable frame
    main_canvas = tk.Canvas(root, highlightthickness=0)
    scrollbar = Scrollbar(root, orient=tk.VERTICAL, command=main_canvas.yview)
    scroll_frame = tk.Frame(main_canvas, highlightthickness=0)
    
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    main_canvas.configure(yscrollcommand=scrollbar.set)
    main_canvas.bind('<Configure>', lambda e: main_canvas.configure(
        scrollregion=main_canvas.bbox('all')
    ))
    
    # Place scroll_frame inside canvas
    main_canvas.create_window((0, 0), window=scroll_frame, anchor='nw')
    scroll_frame.bind('<Configure>', lambda e: main_canvas.configure(
        scrollregion=main_canvas.bbox('all')
    ))
    
    # Bind mouse wheel to scroll
    def on_mousewheel(event):
        main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    main_canvas.bind('<MouseWheel>', on_mousewheel)
    
    padding = 20
    section_gap = 15
    
    # Title
    title_lbl = tk.Label(scroll_frame, text="RightClickResizer", 
                        font=('Segoe UI', 16, 'bold'))
    title_lbl.pack(pady=(padding, 5))
    
    subtitle_lbl = tk.Label(scroll_frame, text="Image Resizer & Video Converter",
                           font=('Segoe UI', 9), fg='#666')
    subtitle_lbl.pack(pady=(0, section_gap))
    
    # Image Settings Section
    img_header = tk.Label(scroll_frame, text="Image Settings", 
                         font=('Segoe UI', 11, 'bold'), fg='#2c7be5')
    img_header.pack(pady=(0, 8))
    
    img_frame = tk.LabelFrame(scroll_frame, text="Resize Options", 
                             font=('Segoe UI', 9), padx=15, pady=10)
    img_frame.pack(fill=tk.X, padx=padding, pady=5)
    
    # Max Width
    tk.Label(img_frame, text="Max Width:", font=('Segoe UI', 9)).grid(
        row=0, column=0, padx=5, pady=5, sticky='w')
    width_var = tk.Entry(img_frame, font=('Segoe UI', 9), width=12)
    width_var.insert(0, str(config.get("max_width", 1920)))
    width_var.grid(row=0, column=1, padx=5, pady=5)
    
    # Max Height
    tk.Label(img_frame, text="Max Height:", font=('Segoe UI', 9)).grid(
        row=1, column=0, padx=5, pady=5, sticky='w')
    height_var = tk.Entry(img_frame, font=('Segoe UI', 9), width=12)
    height_var.insert(0, str(config.get("max_height", 1080)))
    height_var.grid(row=1, column=1, padx=5, pady=5)
    
    # Quality
    tk.Label(img_frame, text="Quality (1-100):", font=('Segoe UI', 9)).grid(
        row=2, column=0, padx=5, pady=5, sticky='w')
    quality_var = tk.Entry(img_frame, font=('Segoe UI', 9), width=12)
    quality_var.insert(0, str(config.get("quality", 85)))
    quality_var.grid(row=2, column=1, padx=5, pady=5)
    
    # Video Settings Section
    vid_header = tk.Label(scroll_frame, text="Video Settings", 
                         font=('Segoe UI', 11, 'bold'), fg='#2c7be5')
    vid_header.pack(pady=(section_gap, 8))
    
    vid_frame = tk.LabelFrame(scroll_frame, text="Conversion Options", 
                             font=('Segoe UI', 9), padx=15, pady=10)
    vid_frame.pack(fill=tk.X, padx=padding, pady=5)
    
    # CRF
    tk.Label(vid_frame, text="CRF (18-28):", font=('Segoe UI', 9)).grid(
        row=0, column=0, padx=5, pady=5, sticky='w')
    crf_var = tk.Entry(vid_frame, font=('Segoe UI', 9), width=12)
    crf_var.insert(0, str(config.get("video_crf", 23)))
    crf_var.grid(row=0, column=1, padx=5, pady=5)
    tk.Label(vid_frame, text="(lower = better quality)", 
            font=('Segoe UI', 8), fg='#888').grid(
        row=0, column=2, padx=5, pady=5, sticky='w')
    
    # Preset
    tk.Label(vid_frame, text="Preset:", font=('Segoe UI', 9)).grid(
        row=1, column=0, padx=5, pady=5, sticky='w')
    preset_var = tk.StringVar(value=str(config.get("video_preset", "medium")))
    preset_combo = tk.OptionMenu(vid_frame, preset_var, 
        "ultrafast", "faster", "fast", "medium", "slow", "slower")
    preset_combo.config(font=('Segoe UI', 9))
    preset_combo.grid(row=1, column=1, padx=5, pady=5, sticky='w')
    tk.Label(vid_frame, text="(slower = smaller file)", 
            font=('Segoe UI', 8), fg='#888').grid(
        row=1, column=2, padx=5, pady=5, sticky='w')
    
    # Video Max Width
    tk.Label(vid_frame, text="Max Width:", font=('Segoe UI', 9)).grid(
        row=2, column=0, padx=5, pady=5, sticky='w')
    v_width_var = tk.Entry(vid_frame, font=('Segoe UI', 9), width=12)
    v_width_var.insert(0, str(config.get("video_max_width", 1920)))
    v_width_var.grid(row=2, column=1, padx=5, pady=5)
    
    # Video Max Height
    tk.Label(vid_frame, text="Max Height:", font=('Segoe UI', 9)).grid(
        row=3, column=0, padx=5, pady=5, sticky='w')
    v_height_var = tk.Entry(vid_frame, font=('Segoe UI', 9), width=12)
    v_height_var.insert(0, str(config.get("video_max_height", 1080)))
    v_height_var.grid(row=3, column=1, padx=5, pady=5)
    
    def save():
        try:
            new_config = {
                "max_width": int(width_var.get()),
                "max_height": int(height_var.get()),
                "quality": int(quality_var.get()),
                "video_crf": int(crf_var.get()),
                "video_preset": preset_var.get(),
                "video_max_width": int(v_width_var.get()),
                "video_max_height": int(v_height_var.get()),
            }
            save_config(new_config)
            messagebox.showinfo("Success", "Settings saved!")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")
    
    save_btn = tk.Button(scroll_frame, text="Save Settings", 
                        command=save, font=('Segoe UI', 10),
                        bg='#2c7be5', fg='white', activebackground='#1a5bb5',
                        activeforeground='white', bd=0, cursor='hand2',
                        relief=tk.FLAT, padx=20, pady=8)
    save_btn.pack(pady=15, fill=tk.X, padx=padding)
    
    def install():
        if install_context_menu():
            messagebox.showinfo("Success", 
                "Context menu installed!\n\nRight-click on images or videos to use.")
        else:
            messagebox.showerror("Error", "Failed to install. Run as Admin?")
    
    def uninstall():
        if uninstall_context_menu():
            messagebox.showinfo("Success", "Context menu uninstalled!")
        else:
            messagebox.showerror("Error", "Failed to uninstall. Run as Admin?")
    
    btn_frame = tk.Frame(scroll_frame)
    btn_frame.pack(pady=10, padx=padding, fill=tk.X)
    
    install_btn = tk.Button(btn_frame, text="Install Context Menu", 
        command=install, font=('Segoe UI', 9), bg='#28a745', fg='white',
        activebackground='#218838', activeforeground='white', bd=0,
        cursor='hand2', relief=tk.FLAT, padx=10, pady=6)
    install_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
    
    uninstall_btn = tk.Button(btn_frame, text="Uninstall", 
        command=uninstall, font=('Segoe UI', 9), bg='#dc3545', fg='white',
        activebackground='#c82333', activeforeground='white', bd=0,
        cursor='hand2', relief=tk.FLAT, padx=10, pady=6)
    uninstall_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
    
    # Info label
    info_text = "Supported: JPG, PNG, BMP, WebP, GIF | MP4, AVI, MOV, MKV, WMV, FLV, WebM"
    tk.Label(scroll_frame, text=info_text, font=('Segoe UI', 8), 
            fg='#888').pack(pady=(10, padding))
    
    print("GUI setup complete, starting mainloop...")
    root.mainloop()


def main():
    print("RightClickResizer starting...")
    print(f"Arguments: {sys.argv}")
    print(f"Frozen: {getattr(sys, 'frozen', False)}")
    
    # Check if arguments are passed (files to process)
    if len(sys.argv) > 1:
        # Process files
        files = sys.argv[1:]
        config = load_config()
        success_count = 0
        fail_count = 0
        
        for file_path in files:
            if not os.path.isfile(file_path):
                print(f"Error: {file_path} is not a file.")
                continue
            
            _, ext = os.path.splitext(file_path)
            
            if ext.lower() in VIDEO_EXTENSIONS:
                # Convert video to MP4
                if convert_to_mp4(
                    file_path,
                    crf=config.get("video_crf", 23),
                    preset=config.get("video_preset", "medium"),
                    max_width=config.get("video_max_width", 1920),
                    max_height=config.get("video_max_height", 1080)
                ):
                    success_count += 1
                else:
                    fail_count += 1
                    print(f"Error: Failed to convert {file_path}")
            else:
                # Resize image
                if resize_image(
                    file_path,
                    config.get("max_width", 1920),
                    config.get("max_height", 1080),
                    config.get("quality", 85)
                ):
                    success_count += 1
                else:
                    fail_count += 1
                    print(f"Error: Failed to resize {file_path}")
        
        print(f"\nDone! Processed: {success_count}, Failed: {fail_count}")
    else:
        # No arguments, open GUI
        try:
            run_gui()
        except Exception as e:
            print(f"GUI Error: {e}")
            import traceback
            traceback.print_exc()
            input("Press Enter to exit...")


if __name__ == "__main__":
    main()
