import sys
import os
import winreg
import ctypes
import logging

SUPPORTED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp', '.webp', '.gif']

def log_install(message):
    print(message)
    if getattr(sys, 'frozen', False):
        exe_dir = os.path.dirname(sys.executable)
    else:
        exe_dir = os.path.dirname(__file__)
    log_path = os.path.join(exe_dir, "install.log")
    with open(log_path, "a") as f:
        f.write(message + "\n")

def get_progid(extension):
    try:
        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, extension) as key:
            progid, _ = winreg.QueryValueEx(key, "")
            return progid
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Warning: Error looking up ProgID for {extension}: {e}")
        return None

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def _cleanup_global_context_menu():
    """Attempts to delete global context menu registry keys if they exist."""
    keys_to_delete = [
        r"*\shell\RightClickResizer\command",
        r"*\shell\RightClickResizer",
        r"AllFilesystemObjects\shell\RightClickResizer\command",
        r"AllFilesystemObjects\shell\RightClickResizer",
    ]
    deleted = False
    for key_path in keys_to_delete:
        # Delete from HKEY_CLASSES_ROOT
        try:
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, key_path)
            deleted = True
        except (FileNotFoundError, OSError):
            pass
        # Delete from HKEY_CURRENT_USER\Software\Classes
        try:
            hkcu_path = "Software\\Classes\\" + key_path
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, hkcu_path)
            deleted = True
        except (FileNotFoundError, OSError):
            pass
    if deleted:
        print("Global context menu keys cleaned up.")
    else:
        print("No global context menu keys found.")

def install_context_menu():
    if not is_admin():
        print("Admin rights required to install context menu.")
        return False

    _cleanup_global_context_menu()
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

        log_install(f"Using exe_path: {exe_path}")

        registered_count = 0
        for ext in SUPPORTED_EXTENSIONS:
            # Use SystemFileAssociations to register directly under the extension
            # This makes the context menu appear for all files with that extension
            # regardless of their ProgID
            key_path = f"SystemFileAssociations\\{ext}\\shell\\RightClickResizer"
            
            log_install(f"Registering context menu for {ext} using SystemFileAssociations")
            
            # Create key
            key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_path)
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "Resize Image")
            winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, "imageres.dll,-5100") # Generic image icon
            winreg.CloseKey(key)
            
            # Command key
            command_key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, f"{key_path}\\command")
            # "%1" passes the file path
            cmd_str = f'{exe_path} "%1"'
            winreg.SetValueEx(command_key, "", 0, winreg.REG_SZ, cmd_str)
            winreg.CloseKey(command_key)
            registered_count += 1
        
        log_install(f"Registered {registered_count}/{len(SUPPORTED_EXTENSIONS)} extensions.")
        log_install("Context menu installed successfully.")
        return True
    except Exception as e:
        print(f"Failed to install context menu: {e}")
        return False

def uninstall_context_menu():
    if not is_admin():
        print("Admin rights required to uninstall context menu.")
        return False

    _cleanup_global_context_menu()
    try:
        for ext in SUPPORTED_EXTENSIONS:
            # Use SystemFileAssociations for uninstall as well
            key_path = f"SystemFileAssociations\\{ext}\\shell\\RightClickResizer"
            # Delete command key first
            try:
                winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, f"{key_path}\\command")
            except (FileNotFoundError, OSError):
                pass # Key might not exist
            
            # Delete main key
            try:
                winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, key_path)
            except (FileNotFoundError, OSError):
                pass # Key might not exist
                
        print("Context menu uninstalled successfully.")
        return True
    except Exception as e:
        print(f"Failed to uninstall (or keys not found): {e}")
        return False
