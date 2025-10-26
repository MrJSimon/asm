# -*- coding: utf-8 -*-
"""
Created on Sat Oct 25 16:34:41 2025

@author: jeg_e
"""
from pathlib import Path
import numpy as np
from PIL import Image

from ..image_analysis.image_analysis_tools import ensure_rgba




def setup_current_image(parent):
    """
    Load or create a mask for the current image.

    Parameters
    ----------
    parent : object
        The main application or frame instance containing:
          - filedirectory : str | Path — base directory for outputs
          - img_filenames : list[str | Path] — list of all image paths
          - img_numb : int — current image index
          - lab_color_rgb : list[tuple[int, int, int]] — label colors (RGB)
          - image_c, image_f, image_m, current_image_path — attributes updated here

    Returns
    -------
    None
        Updates parent attributes in place:
        - image_c : PIL.Image (original RGBA)
        - image_f : PIL.Image (mask overlaid)
        - image_m : PIL.Image (mask grayscale)
        - current_image_path : Path
    """

    try:
        # Create masks directory
        masks_folder = Path(parent.filedirectory) / "output" / "masks"
        masks_folder.mkdir(parents=True, exist_ok=True)

        # Get image path
        img_filename = Path(parent.img_filenames[parent.img_numb])

        # Load base image (ensuring RGBA)
        parent.image_c = ensure_rgba(img_filename)
        parent.image_f = parent.image_c.copy()
        parent.current_image_path = img_filename

        # Mask filename/path
        mask_filename = f"{img_filename.stem}_mask.npy"
        mask_path = masks_folder / mask_filename

        # If mask exists → load and overlay
        if mask_path.exists():
            #print(f"Loading existing mask: {mask_path.name}")
            mask_array = np.load(mask_path)
            parent.image_m = Image.fromarray(mask_array.astype(np.uint8), mode="L")

            img_array = np.array(parent.image_f)
            mask_data = np.array(parent.image_m)

            # Overlay mask colors (skip background 0)
            for label_idx, rgb in enumerate(parent.lab_color_rgb, start=1):
                img_array[mask_data == label_idx, :3] = rgb

            parent.image_f = Image.fromarray(img_array, mode="RGBA")

        else:
            # No mask found → create blank mask
            #print(f"No mask found for {img_filename.name}, creating new blank mask.")
            parent.image_m = Image.new("L", parent.image_c.size, 0)

    except Exception as e:
        print(f"[ERROR] Failed to load or create mask: {e}")
