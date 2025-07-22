"""The module loads images into the GUI for segmentation"""
#import os
from pathlib import Path
from tkinter import filedialog
from tkinter import ttk
import tkinter as tk
#import cv2
import numpy as np

class ImageLoader(ttk.Frame):
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
        self.place(x=5, y=5, relwidth=0.15, relheight=0.08)  #5
        self.create_widget(parent)

    def create_widget(self, parent):
        """
        Create a header label above and an inline row with label, entry, and browse button.
        """
        # HEADER TITLE
        l = ttk.Label(self, text="📂 Image Loader",
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
        self.entry_box = ttk.Entry(frame_top, font=("Segoe UI", 12))  # Save reference
        self.entry_box.insert(0, "C:/Users/.../Images")
        self.entry_box.grid(row=0, column=1, sticky="ew", padx=(0, 5), ipady=0)

        # Browse button
        btn_browser = tk.Button(frame_top, text="Browse",
                                font=("Segoe UI", 10),
                                relief="solid", bd=1,  # Solid border
                                highlightthickness=1,
                                padx=20, pady=0,       # Reduce vertical padding
                                height=1,             # Force button height to match entry
                                command=lambda: self.clicked_filepath(self.entry_box, parent))
        btn_browser.grid(row=0, column=2, sticky="ew")

    @staticmethod
    def sort_names(names_i):
        """
        Sort the image names.

        Args:
            names_i (list): List of image names.

        Returns:
            list: Sorted list of image names.
        """
        tlist = []
        for tstring in names_i:
            tlist.append(int(tstring.split('_')[1].split('.')[0]))
        sort_index = np.argsort(tlist)
        tlist = [names_i[i] for i in sort_index]
        return tlist

    def clicked_filepath(self, e, parent):
        """
        Handle the click event for selecting a file path.

        Args:
            e (ttk.Entry): The entry widget.
            parent: The parent object.
        """
        # Ask for directory
        selected_dir = filedialog.askdirectory()
        if not selected_dir:
            return  # User cancelled

        # Set and normalize path
        parent.filedirectory = Path(selected_dir).resolve()
        e.delete(0, 'end')
        e.insert(0, str(parent.filedirectory))

        # Clear previous lists
        parent.img_filenames = []
        parent.img_name = []

        # Allowed image extensions
        allowed_ext = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"}

        # Get all files and filter for images
        all_files = list(parent.filedirectory.glob("*"))
        image_files = [f for f in all_files if f.suffix.lower() in allowed_ext and f.is_file()]

        # Sort image names
        image_files = self.sort_names([f.name for f in image_files])

        # Append filenames and names to parent lists
        for img_name in image_files:
            img_path = parent.filedirectory / img_name
            parent.img_filenames.append(str(img_path))
            parent.img_name.append(Path(img_name).stem)

        print(f'Images have been loaded: {len(parent.img_filenames)} files found.')

        # 🔥 Refresh AutomationImageSelector if it exists
        if hasattr(parent, 'automation_image_selector'):
            parent.automation_image_selector.refresh(parent)

    def refresh(self, parent):
        """
        Update the entry box to display parent.filedirectory.

        Args:
            parent: The parent widget.
        """
        if not hasattr(parent, 'filedirectory') or not parent.filedirectory:
            print("No directory set in parent. Entry box not updated.")
            return

        self.entry_box.delete(0, 'end')
        self.entry_box.insert(0, str(parent.filedirectory))
        print(f"Entry box updated with {parent.filedirectory}")


        