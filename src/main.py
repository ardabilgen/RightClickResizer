import sys
import os
import tkinter as tk
from tkinter import messagebox
from config import load_config, save_config
from resizer import resize_image
from installer import install_context_menu, uninstall_context_menu, is_admin
import ctypes

def run_gui():
    root = tk.Tk()
    root.title("RightClickResizer Settings")
    root.geometry("300x250")
    
    config = load_config()
    
    tk.Label(root, text="Max Width:").pack(pady=5)
    width_var = tk.Entry(root)
    width_var.insert(0, str(config.get("max_width", 1920)))
    width_var.pack()
    
    tk.Label(root, text="Max Height:").pack(pady=5)
    height_var = tk.Entry(root)
    height_var.insert(0, str(config.get("max_height", 1080)))
    height_var.pack()

    tk.Label(root, text="Quality (1-100):").pack(pady=5)
    quality_var = tk.Entry(root)
    quality_var.insert(0, str(config.get("quality", 85)))
    quality_var.pack()
    
    def save():
        try:
            new_config = {
                "max_width": int(width_var.get()),
                "max_height": int(height_var.get()),
                "quality": int(quality_var.get())
            }
            save_config(new_config)
            messagebox.showinfo("Success", "Settings saved!")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")

    tk.Button(root, text="Save Settings", command=save).pack(pady=10)
    
    def install():
        if install_context_menu():
            messagebox.showinfo("Success", "Context menu installed!")
        else:
            messagebox.showerror("Error", "Failed to install. Run as Admin?")

    def uninstall():
        if uninstall_context_menu():
            messagebox.showinfo("Success", "Context menu uninstalled!")
        else:
            messagebox.showerror("Error", "Failed to uninstall. Run as Admin?")

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=5)
    tk.Button(btn_frame, text="Install Context Menu", command=install).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Uninstall", command=uninstall).pack(side=tk.LEFT, padx=5)

    root.mainloop()

def main():
    # Check if arguments are passed (files to resize)
    if len(sys.argv) > 1:
        # Process files
        files = sys.argv[1:]
        config = load_config()
        success_count = 0
        
        for file_path in files:
            if os.path.isfile(file_path):
                if resize_image(file_path, config["max_width"], config["max_height"], config["quality"]):
                    success_count += 1
        
        # Optional: Show a toast or small popup if desired, but for now just exit.
        # If we want to be silent, we just exit.
        # Maybe print to stdout for debugging.
        print(f"Processed {success_count} files.")
    else:
        # No arguments, open GUI
        run_gui()

if __name__ == "__main__":
    # If not admin and trying to run GUI (which might need admin for install), 
    # we could auto-elevate, but let's keep it simple and let user handle it or show error.
    main()
