import os
import sys
import winreg
from core.constants import APP_NAME

def get_app_data_dir():
    """Get the persistent app data directory in %APPDATA%."""
    app_data = os.getenv('APPDATA')
    path = os.path.join(app_data, APP_NAME)
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    return path

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if getattr(sys, 'frozen', False):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    # Prioritize items in the executable directory (for data storage)
    if getattr(sys, 'frozen', False):
        exe_dir_path = os.path.join(os.path.dirname(sys.executable), relative_path)
        if os.path.exists(exe_dir_path):
            return exe_dir_path

    return os.path.join(base_path, relative_path)

def is_windows_dark_mode():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                           r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        winreg.CloseKey(key)
        return value == 0
    except Exception:
        return False

def is_startup_enabled():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Microsoft\Windows\CurrentVersion\Run",
                             0, winreg.KEY_READ)
        winreg.QueryValueEx(key, APP_NAME)
        winreg.CloseKey(key)
        return True
    except (FileNotFoundError, OSError):
        return False

def enable_startup():
    try:
        # Use CreateKeyEx to ensure the path exists and it's open for writing
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE) as key:
            if getattr(sys, 'frozen', False):
                app_path = sys.executable
                # Direct registry entry for exe
                winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, f'"{app_path}"')
            else:
                # Get the absolute path of the calling script
                if '__main__' in sys.modules and hasattr(sys.modules['__main__'], '__file__'):
                    app_path = os.path.abspath(sys.modules['__main__'].__file__)
                else:
                    app_path = os.path.abspath(sys.argv[0])
                
                # Use a .bat in AppData for script mode to avoid CWD issues
                bat_path = os.path.join(get_app_data_dir(), f"{APP_NAME}.bat")
                with open(bat_path, "w") as bat_file:
                    bat_file.write(f'@echo off\ncd /d "{os.path.dirname(app_path)}"\n"{sys.executable}" "{app_path}"')
                winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, f'"{bat_path}"')
            
        return True, "开机自启动已启用！"
    except Exception as e:
        return False, f"无法设置开机自启动: {e}"

def disable_startup():
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE) as key:
            try:
                winreg.DeleteValue(key, APP_NAME)
            except FileNotFoundError:
                pass # Already deleted
        
        bat_path = os.path.join(get_app_data_dir(), f"{APP_NAME}.bat")
        if os.path.exists(bat_path):
            try:
                os.remove(bat_path)
            except: pass
            
        return True, "开机自启动已禁用！"
    except FileNotFoundError:
        return True, "开机自启动已禁用！"
    except Exception as e:
        return False, f"无法取消开机自启动: {e}"

def toggle_startup(enable):
    if enable:
        return enable_startup()
    else:
        return disable_startup()
