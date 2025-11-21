import sys
import os
import winreg
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def install_context_menu():
    if not is_admin():
        print("Admin rights required to install context menu.")
        return False

    try:
        # Get the path to the executable
        if getattr(sys, 'frozen', False):
            exe_path = sys.executable
        else:
            # For development, use python executable + script path
            # But for the final context menu, we usually want the built exe.
            # If running from source, we might point to a bat file or python command.
            # For simplicity in this script, we'll assume we are setting it up for the current running method.
            # However, the user requested a "setup" program. 
            # Let's point to the current python script for now if not frozen.
            exe_path = f'"{sys.executable}" "{os.path.abspath(os.path.join(os.path.dirname(__file__), "main.py"))}"'

        # Key for all files
        key_path = r"*\shell\RightClickResizer"
        
        # Create key
        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_path)
        winreg.SetValue(key, "", winreg.REG_SZ, "Resize Image")
        winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, "imageres.dll,-5100") # Generic image icon
        winreg.CloseKey(key)
        
        # Command key
        command_key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, f"{key_path}\\command")
        # "%1" passes the file path
        cmd_str = f'{exe_path} "%1"'
        winreg.SetValue(command_key, "", winreg.REG_SZ, cmd_str)
        winreg.CloseKey(command_key)
        
        print("Context menu installed successfully.")
        return True
    except Exception as e:
        print(f"Failed to install context menu: {e}")
        return False

def uninstall_context_menu():
    if not is_admin():
        print("Admin rights required to uninstall context menu.")
        return False

    try:
        key_path = r"*\shell\RightClickResizer"
        # Delete command key first
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, f"{key_path}\\command")
        # Delete main key
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, key_path)
        print("Context menu uninstalled successfully.")
        return True
    except Exception as e:
        print(f"Failed to uninstall (or keys not found): {e}")
        return False
