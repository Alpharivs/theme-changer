from configparser import ConfigParser
import ctypes
import datetime
import pathlib
import sys
import winreg

KEY_PATH = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize"

def get_configuration():
    # Open config.ini and get the desired settings.
    configure = ConfigParser()
    configure.read('config.ini')

    night_mode_time = configure.getint('Settings', 'NightModeTime')
    light_mode_time = configure.getint('Settings', 'LightModeTime')
    image_path = configure.get('Settings', 'imagepath')
    return night_mode_time, light_mode_time, image_path

def get_current_value():
    # Query one of the two required values for night mode and check it's value.
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, KEY_PATH)
        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        winreg.CloseKey(key)
        return value
    # Error handling is done this way because the script is meant to run as scheduled task so there's no point in outputing error.
    except Exception:
        return None
    
def mode_check():
    # Get the current time and convert the settings to the appropiate format.
    now = datetime.datetime.now().time()
    light_mode_conv = datetime.time(light_mode_time,00)
    night_mode_conv = datetime.time(night_mode_time,00)

    # 0 is night mode 1 is light mode.
    # This checks if the current time is the same as the desired time for night mode, without this it was not activating at the same hour.
    if now == night_mode_conv:
            return 0
    # This conditions make it so that even with time wrapping a value like 18:00 will still be treated as night mode after 00:00 until the light mode time.
    elif light_mode_conv < night_mode_conv:
        if now >= light_mode_conv and now <= night_mode_conv:
            return 1
        else:
            return 0

def set_registry_value(value_name, value):
    # Change the desired values in the registry.
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, KEY_PATH, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, value)
        winreg.CloseKey(key)
    except Exception:
        return None

def get_filename():
    folder_path = pathlib.Path(image_path)
    # Iterate the images folder and choose the night wallpaper for night mode and the light one for light mode.
    for file_path in folder_path.iterdir():
        if file_path.is_file():
            if value == 0 and 'night' in file_path.name:
                return file_path.name
            elif value == 1 and 'light' in file_path.name:
                return file_path.name
        
def change_theme(value):
    # Call functions to change the desired registry values.
    set_registry_value("AppsUseLightTheme", value)
    set_registry_value("SystemUsesLightTheme", value)
    # Set the appropiate wallpaper for the theme.
    wallpaper_name = get_filename()
    ctypes.windll.user32.SystemParametersInfoW(20, 0, f"{image_path}{wallpaper_name}" , 0)

if __name__ == "__main__":
    # Set variables from values in the config.ini file.
    night_mode_time, light_mode_time, image_path = get_configuration()
    # Check the current values of the registry.
    current_value = get_current_value()
    # Set the value variable according to the desired hours and check if that theme is not already set.
    value = mode_check()
    if value == current_value:
        sys.exit(1)
    change_theme(value)