# -*- coding: utf-8 -*-
"""
Created on Tue Jul 22 12:35:58 2025

@author: jeg_e
"""
import PIL.Image
import PIL.ImageTk
import PIL.Image
import PIL.ImageDraw
import PIL
from pathlib import Path
import numpy as np

@staticmethod
def ensure_rgba(image_path):
    """
    Load an image and ensure it is in RGBA format.

    Args:
        image_path (str or Path): Path to the image file.

    Returns:
        PIL.Image.Image: Image converted to RGBA format.
    """
    # Load image
    img = PIL.Image.open(image_path)
    name = Path(image_path).name

    print(f"Loaded {name} with mode {img.mode}")

    if img.mode == 'RGBA':
        print(f"{name}: Already RGBA")
        return img

    elif img.mode == 'RGB':
        print(f"{name}: RGB → RGBA")
        return img.convert('RGBA')

    elif img.mode == 'L':
        print(f"{name}: Grayscale (L) → RGBA")
        return img.convert('RGBA')

    elif img.mode.startswith('I;16') or img.mode == 'I':
        print(f"{name}: High bit-depth ({img.mode}) → normalize → RGBA")
        # Convert to numpy array and normalize to 0-255
        arr = np.array(img, dtype=np.uint16)  # Read as 16-bit array
        arr_8bit = (arr / 256).astype(np.uint8)  # Scale to 8-bit range
        img_8bit = PIL.Image.fromarray(arr_8bit, mode='L')  # Back to PIL Image
        return img_8bit.convert('RGBA')

    else:
        print(f"{name}: Unexpected mode ({img.mode}) → forcing RGBA")
        return img.convert('RGBA')