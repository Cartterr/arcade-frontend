from PIL import Image
import pygame
import io
from win32con import LR_DEFAULTSIZE, LR_LOADFROMFILE
from win32gui import ExtractIconEx, DestroyIcon
from win32ui import CreateBitmap, CreateDCFromHandle
import pylnk3 as lnk
import configparser
import os
import subprocess

def get_target_exe_path_lnk(shortcut_path):
    print(shortcut_path)
    with open(shortcut_path, 'rb') as stream:
        lnk_file = lnk.parse(stream)
        return lnk_file.target

def get_target_exe_path_url(shortcut_path):
    config = configparser.ConfigParser()
    config.read(shortcut_path)
    return config['InternetShortcut']['URL']

def extract_icon_from_exe(exe_path):
    icon_path = exe_path + ".ico"
    # Replace 'extract_icon_tool' with the actual command of your icon extraction tool
    subprocess.run(['extract_icon_tool', exe_path, icon_path], check=True)
    if os.path.exists(icon_path):
        icon_surface = pygame.image.load(icon_path).convert_alpha()
        return icon_surface
    return None

def ico_to_surface(ico_path):
    """Assuming this function loads an icon file into a pygame.Surface."""
    try:
        return pygame.image.load(ico_path).convert_alpha()
    except Exception as e:
        print(f"Error loading icon {ico_path}: {e}")
        return None
    
def extract_icon(exe_path, size=(32, 32)):
    # Extracts the first icon from an executable
    large, small = ExtractIconEx(exe_path, 0)
    # Use the appropriate icon size (large or small)
    handle = small[0] if size == (16, 16) else large[0]
    # Create a PyCBitmap from the icon handle
    bmp = CreateBitmap()
    bmp.Attach(handle)
    # Convert the PyCBitmap to a Pygame surface
    hdcBitmap = bmp.GetHandle()
    hdcScreen = CreateDCFromHandle(hdcBitmap)
    surface = pygame.image.frombuffer(bmp.GetBitmapBits(True), bmp.GetSize(), 'RGBA')
    # Cleanup
    for icon in large + small:
        DestroyIcon(icon)
    return surface