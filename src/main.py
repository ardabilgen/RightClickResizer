import sys
import os
import tkinter as tk
from tkinter import messagebox, ttk
from config import load_config, save_config
from resizer import resize_image
from video_converter import convert_to_mp4, VIDEO_EXTENSIONS
from context_menu import install_context_menu, uninstall_context_menu, is_admin, IMAGE_EXTENSIONS, ALL_EXTENSIONS
import ctypes


def is_video_file(file_path):
    """Check if a file is a video based on extension."""
    _, ext = os.path.splitext(file_path)
    return ext.lower() in VIDEO_EXTENSIONS


def run_gui():
    root = tk.Tk()
    root.title("RightClickResizer — Image & Video Tool")
    root.geometry("450x550")
    
    config = load_config()
    
    # Modern styling
    style = ttk.Style()
    style.configure('TLabel', font=('Segoe UI', 10))
    style.configure('Header.TLabel', font=('Segoe UI', 12, 'bold'))
    style.configure('Section.TLabel', font=('Segoe UI', 10, 'bold'), foreground='#2c7be5')
    style.configure('Button', font=('Segoe UI', 9))
    
    # Main container with scrollbar
    main_frame = ttk.Frame(root, padding=15)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    canvas = tk.Canvas(main_frame, highlightthickness=0)
    scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollable = ttk.Frame(canvas)
    
    scrollbar.configure(command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollable_window = canvas.window_create(0, 0, window=scrollable, anchor='nw')
    
    scrollable.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    
    # Title
    ttk.Label(scrollable, text="⚡ RightClickResizer", style='Header.TLabel').pack(pady=(0, 15))
    
    # ─── Image Settings Section ───
    ttk.Label(scrollable, text="🖼️  Image Settings", style='Section.TLabel').pack(pady=(10, 5))
    
    img_frame = ttk.LabelFrame(scrollable, text="Resize Options", padding=10)
    img_frame.pack(fill=tk.X, pady=5)
    
    # Max Width
    ttk.Label(img_frame, text="Max Width:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
    width_var = ttk.Entry(img_frame, width=10)
    width_var.insert(0, str(config.get("max_width", 1920)))
    width_var.grid(row=0, column=1, padx=5, pady=5)
    
    # Max Height
    ttk.Label(img_frame, text="Max Height:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
    height_var = ttk.Entry(img_frame, width=10)
    height_var.insert(0, str(config.get("max_height", 1080)))
    height_var.grid(row=1, column=1, padx=5, pady=5)
    
    # Quality
    ttk.Label(img_frame, text="Quality (1-100):").grid(row=2, column=0, padx=5, pady=5, sticky='w')
    quality_var = ttk.Entry(img_frame, width=10)
    quality_var.insert(0, str(config.get("quality", 85)))
    quality_var.grid(row=2, column=1, padx=5, pady=5)
    
    # ─── Video Settings Section ───
    ttk.Label(scrollable, text="🎬 Video Settings", style='Section.TLabel').pack(pady=(10, 5))
    
    vid_frame = ttk.LabelFrame(scrollable, text="Conversion Options", padding=10)
    vid_frame.pack(fill=tk.X, pady=5)
    
    # CRF
    ttk.Label(vid_frame, text="CRF (18-28):").grid(row=0, column=0, padx=5, pady=5, sticky='w')
    crf_var = ttk.Entry(vid_frame, width=10)
    crf_var.insert(0, str(config.get("video_crf", 23)))
    crf_var.grid(row=0, column=1, padx=5, pady=5)
    ttk.Label(vid_frame, text="(lower = better quality)").grid(row=0, column=2, padx=5, pady=5, sticky='w')
    
    # Preset
    ttk.Label(vid_frame, text="Preset:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
    preset_var = ttk.Combobox(vid_frame, values=["ultrafast", "faster", "fast", "medium", "slow", "slower"], width=8)
    preset_var.set(str(config.get("video_preset", "medium")))
    preset_var.grid(row=1, column=1, padx=5, pady=5)
    ttk.Label(vid_frame, text="(slower = smaller file)").grid(row=1, column=2, padx=5, pady=5, sticky='w')
    
    # Video Max Width
    ttk.Label(vid_frame, text="Max Width:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
    v_width_var = ttk.Entry(vid_frame, width=10)
    v_width_var.insert(0, str(config.get("video_max_width", 1920)))
    v_width_var.grid(row=2, column=1, padx=5, pady=5)
    
    # Video Max Height
    ttk.Label(vid_frame, text="Max Height:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
    v_height_var = ttk.Entry(vid_frame, width=10)
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
    
    ttk.Button(scrollable, text="💾  Save Settings", command=save).pack(pady=10, fill=tk.X)
    
    def install():
        if install_context_menu():
            messagebox.showinfo("Success", "Context menu installed!\n\nRight-click on images or videos to use.")
        else:
            messagebox.showerror("Error", "Failed to install. Run as Admin?")
    
    def uninstall():
        if uninstall_context_menu():
            messagebox.showinfo("Success", "Context menu uninstalled!")
        else:
            messagebox.showerror("Error", "Failed to uninstall. Run as Admin?")
    
    btn_frame = ttk.Frame(scrollable)
    btn_frame.pack(pady=10, fill=tk.X)
    ttk.Button(btn_frame, text="🔧  Install Context Menu", command=install).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
    ttk.Button(btn_frame, text="🗑️  Uninstall", command=uninstall).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
    
    # Info label
    info_text = "Supported: JPG, PNG, BMP, WebP, GIF | MP4, AVI, MOV, MKV, WMV, FLV, WebM"
    ttk.Label(scrollable, text=info_text, font=('Segoe UI', 8), foreground='#888').pack(pady=5)


def main():
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
        run_gui()


if __name__ == "__main__":
    main()
