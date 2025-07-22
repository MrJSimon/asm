# -*- coding: utf-8 -*-
"""
Created on Tue Jul 22 09:41:37 2025

@author: jeg_e
"""
"""The module loads images into the GUI for segmentation"""
#import os
from pathlib import Path
from tkinter import filedialog
from tkinter import ttk
import tkinter as tk
#import numpy as np
import json

class JsonLoader(ttk.Frame):
    """
    A frame for loading images into the main frame window.

    Attributes:
        parent (tk.Tk): The parent window.
        filepath (str): The selected file path.
    """

    def __init__(self, parent):
        """
        Initialize ImageLoader frame.

        Args:
            parent (tk.Tk): The parent window.
        """
        super().__init__(parent, borderwidth=2, relief="solid")
        self.place(relx = 0.165, y=5, relwidth=0.15, relheight=0.08) #5
        self.create_widget(parent)

    def create_widget(self, parent):        
        
        """
        Create a header label above and an inline row with label, entry, and browse button.
        """
        # HEADER TITLE
        l = ttk.Label(self, text="📂 Json Loader", 
              font=('Times', 24), anchor="w")
        l.pack(fill="x", padx=5, pady=(5, 10))  # Top padding for separation
        
        # INLINE ROW FRAME
        frame_top = ttk.Frame(self)
        frame_top.pack(fill='x', padx=5, pady=5)
        
        frame_top.columnconfigure(1, weight=1)  # Entry expands
        
        # Small inline label ("Path")
        path_label = ttk.Label(frame_top, text="Path", font=("Segoe UI", 12))
        path_label.grid(row=0, column=0, sticky="w", padx=(0, 5))
        
        # Entry field
        e = ttk.Entry(frame_top, font=("Segoe UI", 12))
        e.insert(0, "C:/Users/.../json")
        e.grid(row=0, column=1, sticky="ew", padx=(0, 5), ipady=0)  # Add ipady=1 to slightly increase internal height
        
        # Browse button
        btn_browser = tk.Button(frame_top, text="Browse",
                                font=("Segoe UI", 10),
                                relief="solid", bd=1,  # Solid border
                                highlightthickness=1,
                                padx=20, pady=0,       # Reduce vertical padding
                                height=1,             # Force button height to match entry
                                command=lambda: self.clicked_filepath(e, parent))
        btn_browser.grid(row=0, column=2, sticky="ew")
    
    def clicked_filepath(self, e, parent):
        """
        Handle the click event for selecting a file path.
    
        Args:
            e (ttk.Entry): The entry widget.
            parent: The parent object.
        """
        # Ask for directory
        selected_dir = filedialog.askopenfilename(
            title="Select Training Set JSON",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not selected_dir:
            return  # User cancelled
    
        # Set and normalize path
        filepath = Path(selected_dir).resolve()
        e.delete(0, 'end')
        e.insert(0, str(filepath))
    
        # Load JSON data
        with open(filepath, 'r') as f:
            data = json.load(f)
    
        # Restore the parent entries with what is expected to be in json
        parent.filedirectory = Path(data.get("filepath"))
        parent.img_filenames = data.get("images")
        parent.training_image_paths = data.get("training images", [])
        parent.training_mask_paths = data.get("training masks", [])
        parent.lab_name = data["labels"]
        selected_features = data.get("features", [])
        
        # Restore selected features in GUI
        print("Restoring selected features:", selected_features)
        for feature, var in parent.feature_selector.feature_vars.items():
            var.set(feature in selected_features)

        # Refresh UI if Training Set Manager exists
        if hasattr(parent, 'training_set_manager'):
            parent.training_set_manager.refresh()
        
        # 🔥 Refresh AutomationImageSelector if it exists
        if hasattr(parent, 'automation_image_selector'):
            parent.automation_image_selector.refresh(parent)
            
        # 🔥 Refresh labelmanager if it exists
        if hasattr(parent, 'label_manager_labels'):
            parent.label_manager_labels.refresh(parent)
            
        # 🔥 Refresh imageloader if it exists
        if hasattr(parent, 'image_loader'):
            parent.image_loader.refresh(parent)
        
        
class JsonSaver(ttk.Frame):
    """
    Frame widget for saving and loading the training set as JSON.
    """
    def __init__(self, parent):
        """
        Initialize SaveLoadJSON frame and place it within the parent widget.

        Args:
            parent: The parent widget.
        """
        super().__init__(parent)
        self.place(
            x=5.0,
            rely=0.095 + 0.04 + 2.0 * 0.08 + 0.03 + 0.0115 + 0.04 + 0.2 + 0.03 + 0.0115 + 0.04 + 0.2,
            relwidth=0.15,
            relheight=0.03
        )
        self.create_widget(parent)

    def create_widget(self, parent):
        """
        Create and configure the save/load buttons.

        Args:
            parent: The parent widget.
        """
        bt = tk.Button(self, text='save json',
                       font=("Segoe UI", 10),
                       relief="solid", bd=1,
                       highlightthickness=1,
                       padx=20, pady=0,
                       height=1,
                       command=lambda: self.save_training_set(parent))

        bt.pack(side='left', anchor='e', expand=True, fill='both')

    @staticmethod
    def save_training_set(parent, filepath=None):
        """
        Save training set JSON into output folder. Masks are already saved as .npy.
        """
        # Normalize base directory
        base_dir = Path(parent.filedirectory)
    
        # Output folder
        output_folder = base_dir / "output"
        output_folder.mkdir(parents=True, exist_ok=True)
    
        # JSON path
        if filepath is None:
            filepath = output_folder / "training_set.json"
    
        # Prepare JSON data
        data = {"filepath": str(parent.filedirectory),
            "images": parent.img_filenames,  
            "training images": parent.training_image_paths,
            "training masks": parent.training_mask_paths,
            "labels": parent.lab_name,
            "features": parent.feature_selector.get_selected_features()
        }
    
        # Save JSON
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Training set saved to {filepath}")
        
        # def save_training_set(parent, filepath=None):
        #     """
        #     Save training set JSON into output folder. Masks are already saved as .npy.
        #     """
        #     # Normalize base directory
        #     base_dir = Path(parent.filedirectory)
        
        #     # Output folder
        #     output_folder = base_dir / "output"
        #     output_folder.mkdir(parents=True, exist_ok=True)
        
        #     # JSON path
        #     if filepath is None:
        #         filepath = output_folder / "training_set.json"
        
        #     # Prepare JSON data
        #     data = {
        #         "images": parent.training_image_paths,
        #         "masks": parent.training_mask_paths,
        #         "features": parent.feature_selector.get_selected_features()
        #     }
        
        #     # Save JSON
        #     with open(filepath, 'w') as f:
        #         json.dump(data, f, indent=4)
        #     print(f"Training set saved to {filepath}")