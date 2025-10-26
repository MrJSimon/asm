# -*- coding: utf-8 -*-
"""
Created on Sat Oct 25 15:16:35 2025

@author: jeg_e
"""
"""The module loads images into the GUI for segmentation"""
#import os
from pathlib import Path
from tkinter import filedialog
from tkinter import ttk
import tkinter as tk
import numpy as np
import PIL
from ..image_analysis.image_analysis_tools import ensure_rgba
from ..helper_functions.image_utils import setup_current_image

class ImageToogleText(ttk.Frame):
    """
    A frame for loading images into the main frame window.

    Attributes:
        parent (tk.Tk): The parent window.
        filepath (str): The selected file path.
    """

    def __init__(self, parent):
        """
        Initialize LabelManagerText frame and place it within the parent widget.

        Args:
            parent: The parent widget.
        """
        super().__init__(parent,borderwidth=2, relief="solid")
        self.place(relx=0.165, 
                   rely=0.55 + 0.06 + 0.3,
                   relwidth=0.15, relheight=0.04)
        self.create_widget(parent)

    def create_widget(self, parent):
        """
        Create and configure the label widget.

        Args:
            parent: The parent widget.
        """
        #HEADER TITLE
        l = ttk.Label(self, text="Image toogle", 
              font=('Times', 24), anchor="w", justify="left")
        l.grid(row=0, column=0, sticky='w', padx=5, pady=(5, 10))
        
class ImageToogle(ttk.Frame):
    """
    Frame widget for automating RF predictions over all images with progress bar.
    """
    def __init__(self, parent):
        """
        Initialize AutomationManager frame.
        """
        super().__init__(parent)
        self.place(relx=0.165,
                   rely=0.55 + 0.06 + 0.3+0.04,
                   relwidth=0.15, 
                   relheight=0.03)
        self.create_widget(parent)

    def create_widget(self, parent):
        """
        Create header label, automation button, and progress bar.
        """

        # Go to image when button has been pushed
        btn_run = tk.Button(self, text="Go to image",
                            font=("Segoe UI", 10),
                            relief="solid", bd=1,
                            highlightthickness=1,
                            padx=20, pady=0,
                            height=1,
                            command=lambda: self.run_toogle(parent))


        # INLINE ROW FRAME
        #frame_top = tk.Frame(self)
        
        
        #btn_run = tk.Button(self, text="Toggle image", command=lambda: self.run_toogle(parent))
        self.entry_box = tk.Entry(self, font=("Segoe UI", 10))            # <-- parent is self
        self.entry_box.insert(0, "'Insert image number'")
       
        # layout
        btn_run.pack(side='right', expand=True, fill='both')
        self.entry_box.pack(side='left', expand=True, fill='both')
        
        
        
        #self.entry_box = tk.Entry(frame_top, font=("Segoe UI", 10))
        #self.entry_box.insert(0, "C:/Users/.../Images")
        
        
        # Progress bar
        #self.progress_bar = ttk.Progressbar(self, orient="horizontal",
                                            #mode="determinate", maximum=100)
        #self.progress_bar.pack(fill="x", padx=10, pady=(5, 0))
        
        #btn_run.pack(side='left', anchor='e', expand=True, fill='both')
        #self.entry_box.pack(side='right', anchor='w', expand=True, fill='both')
        
        
    def run_toogle(self, parent):
        
        # Get number of images in stack
        n_images = len(parent.img_filenames)
        
        # Get information inside entry-box
        info = self.entry_box.get()
        
        
        try:
            # Try to convert to float first (handles things like "3.0" or "2.5")
            value = float(info)
            
            # Check if it's an integer value (e.g. 3.0 == 3)
            if value.is_integer():
                index = int(value)
                print(f"Valid integer index: {index}")
                
                parent.img_numb = index
                
                setup_current_image(parent)
                
                parent.image_window.refresh_from_parent(parent)
                
            else:
                # Handle non-integer float input
                self.entry_box.delete(0, 'end')
                self.entry_box.insert(0, "Please insert an integer between 0 - " + str(n_images))
                
        except ValueError:
            # Handle anything that can't be converted to a number
            #print(f"'{info}' is not a valid number.")
            self.entry_box.delete(0, 'end')
            self.entry_box.insert(0, "Please insert an integer between 0 - " + str(n_images))
            
        
        #if index.is_integer():
            
            
        #    setup_current_image(parent)
            
            
            # # Create directory string to the mask folder
            # masks_folder = Path(parent.filedirectory) / "output" / "masks"
            # masks_folder.mkdir(parents=True, exist_ok=True)
            
            # # Get the new image
            # img_filename = parent.img_filenames[parent.img_numb]
            
            # #parent.image_c = PIL.Image.open(img_filename)
            
            # parent.image_c = ensure_rgba(img_filename)
            # parent.image_f = parent.image_c.copy()
        
            # # Set current image path
            # parent.current_image_path = img_filename
        
            # # Create mask file name for new image
            # mask_filename = Path(parent.current_image_path).stem + '_mask.npy'
            # mask_path = masks_folder / mask_filename
        
            # # Check if mask exists
            # if mask_path.exists():
            #     print(f"Loading existing mask: {mask_path.name}")
            #     mask_array = np.load(mask_path)
            #     parent.image_m = PIL.Image.fromarray(mask_array.astype(np.uint8), mode="L")
        
            #     # Impose mask on image_f
            #     img_array = np.array(parent.image_f)
            #     mask_data = np.array(parent.image_m)
        
            #     # Replace RGB values at mask indices with corresponding colors
            #     for label_idx, rgb in enumerate(parent.lab_color_rgb, start=1):
            #         img_array[mask_data == label_idx, :3] = rgb  # Replace only RGB channels
        
            #     # Convert back to PIL after NumPy modification
            #     parent.image_f = PIL.Image.fromarray(img_array, mode="RGBA")
            # else:
            #     #print(f"No mask found for {parent.current_image_path}, creating blank mask.")
            #     parent.image_m = PIL.Image.new("L", parent.image_c.size, 0)
        
            # Call image window to display the image
            
        

        
        
        # # Try to convert to float;
        # try:
        #     value = float(info)
        # except TypeError:
        #     oink = 2
        
        # if type(info) != int:
        #     self.entry_box.delete(0, 'end')
        #     self.entry_box.insert(0, "Please insert an integer between 0 - " + str(n_images)) 
        
        # else:
        #     print('Succes will fetch image = ' + int(info))
        
        # Check if info is a string integer
        #try:
        #    check = int(info)
            
        
        #print('this is entry box info' + info)
        
        # Get the new image
        #img_filename = parent.img_filenames[parent.img_numb]
        
        #print('oink oink')