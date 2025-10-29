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
        
        # Create string variable
        self.text_var_toogle = tk.StringVar(value="Image number")
        
        # Create label
        self.label = ttk.Label(self, textvariable=self.text_var_toogle, 
              font=('Times', 24), anchor="w", justify="left")
       
        # Position the label inside the grid
        self.label.grid(row=0, column=0, sticky='w', padx=5, pady=(5, 10))
        
    def update_widget(self, parent):
        
        # Get number of images, subtract one for python syntax
        n_images = len(parent.img_filenames) - 1
        
        # Get image number
        image_number = parent.img_numb
        
        # Create string for input in entry
        text_var = 'Image number ' + str(image_number) + ' / ' + str(n_images)
    
        # Update text dynamically
        self.text_var_toogle.set(text_var)
        

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
        
        
        #btn_run = tk.Button(self, text="Toggle image", command=lambda: self.run_toogle(parent))
        self.entry_box = tk.Entry(self, font=("Segoe UI", 10))            # <-- parent is self
        self.entry_box.insert(0, "'Insert image number'")
       
        # layout
        btn_run.pack(side='right', expand=True, fill='both')
        self.entry_box.pack(side='left', expand=True, fill='both')
        
        
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
                
                parent.image_toogle_text.update_widget(parent)
                
            else:
                # Handle non-integer float input
                self.entry_box.delete(0, 'end')
                self.entry_box.insert(0, "Please insert an integer between 0 - " + str(n_images))
                
        except ValueError:
            # Handle anything that can't be converted to a number
            #print(f"'{info}' is not a valid number.")
            self.entry_box.delete(0, 'end')
            self.entry_box.insert(0, "Please insert an integer between 0 - " + str(n_images))