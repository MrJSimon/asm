
from tkinter import ttk
import tkinter as tk
import numpy as np
from ..randomforest_classifier.training_functions import predict_features
import PIL.Image
from pathlib import Path

from ..image_analysis.image_analysis_tools import ensure_rgba


class AutomationManagerText(ttk.Frame):
    """
    A frame widget for managing labels.

    Attributes:
        parent (ttk.Tk): The parent window.
    """

    def __init__(self, parent):
        """
        Initialize LabelManagerText frame and place it within the parent widget.

        Args:
            parent: The parent widget.
        """
        super().__init__(parent,borderwidth=2, relief="solid")
        self.place(relx=0.165, 
                   rely=0.095 + 0.04 + 2.0 * 0.08 + 0.03 + 0.0115 + 0.04 + 0.2 + 0.03 + 0.0115,
                   relwidth=0.15, relheight=0.04)
        self.create_widget(parent)

    def create_widget(self, parent):
        """
        Create and configure the label widget.

        Args:
            parent: The parent widget.
        """
        #HEADER TITLE
        l = ttk.Label(self, text="🤖 Automation Manager", 
              font=('Times', 24), anchor="w", justify="left")
        l.grid(row=0, column=0, sticky='w', padx=5, pady=(5, 10))

class AutomationImageSelector(ttk.Frame):
    """
    A frame widget for selecting which images to run predictions on.
    """
    def __init__(self, parent):
        super().__init__(parent, borderwidth=0, relief="solid")
        self.place(relx=0.165,
                   rely=0.095 + 0.04 + 2.0 * 0.08 + 0.03 + 0.0115 + 0.04 + 0.2 + 0.03 + 0.0115 + 0.04,
                   relwidth=0.15, relheight=0.2)
        self.create_widget(parent)

    def create_widget(self, parent):
        """
        Create scrollable list of checkboxes with selection controls at the top.
        """
        # Top control bar
        control_frame = tk.Frame(self, borderwidth=0, highlightthickness=0)
        

        # Create buttons
        btn_select_all = tk.Button(control_frame, text="Select All",
                                   font=("Segoe UI", 10),
                                   relief="solid", bd=1,
                                   highlightthickness=1,
                                   padx=20, pady=0,
                                   height=1,
                                   command=lambda: self.select_all(parent))
        btn_deselect_all = tk.Button(control_frame, text="Deselect All",
                                     font=("Segoe UI", 10),
                                     relief="solid", bd=1,
                                     highlightthickness=1,
                                     padx=20, pady=0,
                                     height=1,
                                     command=lambda: self.deselect_all(parent))
        btn_every_second = tk.Button(control_frame, text="Every 2nd",
                                     font=("Segoe UI", 10),
                                     relief="solid", bd=1,
                                     highlightthickness=1,
                                     padx=20, pady=0,
                                     height=1,
                                     command=lambda: self.select_every_second(parent))

        control_frame.pack(side="top", fill="both", expand=True, padx=0, pady=0)  # Full width & height


        # Make grid columns expand equally
        control_frame.columnconfigure(0, weight=1)
        control_frame.columnconfigure(1, weight=1)
        control_frame.columnconfigure(2, weight=1)

        # Place buttons in grid with sticky
        btn_select_all.grid(row=0, column=0, sticky="nsew")
        btn_deselect_all.grid(row=0, column=1, sticky="nsew")
        btn_every_second.grid(row=0, column=2, sticky="nsew")


        # Scrollable frame for image checkboxes
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        self.scroll_frame = tk.Frame(self.canvas)
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=vsb.set)

        vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Storage for image variables
        #self.image_vars = []

    def refresh(self, parent):
        """
        Refresh the list of checkboxes based on parent.img_filenames.
        """
        # Clear old widgets
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        #self.image_vars = []
        for img_path in parent.img_filenames:
            ## Create boolean value for check symbol
            var = tk.BooleanVar(value=True)  # default checked
            ## Create checkbutton
            chk = ttk.Checkbutton(self.scroll_frame, text=Path(img_path).name, variable=var)
            ## Pack the button
            chk.pack(anchor="w", padx=5, pady=2)
            ## Append to the parent
            parent.image_vars.append((img_path, var))

        print(f"✅ Automation selector updated: {len(parent.image_vars)} images listed.")

    def select_all(self,parent):
        """Check all image boxes."""
        for _, var in parent.image_vars:
            var.set(True)
            
    def deselect_all(self,parent):
        """Uncheck all image boxes."""
        for _, var in parent.image_vars:
            var.set(False)

    def select_every_second(self,parent):
        """Select every second image."""
        for i, (_, var) in enumerate(parent.image_vars):
            var.set(i % 2 == 0)

    def get_selected_images(self,parent):
        """Return list of selected image paths."""
        return [img_path for img_path, var in parent.image_vars if var.get()]

class AutomationManager(ttk.Frame):
    """
    Frame widget for automating RF predictions over all images with progress bar.
    """
    def __init__(self, parent):
        """
        Initialize AutomationManager frame.
        """
        super().__init__(parent)
        self.place(relx=0.165,
                   rely=0.095 + 0.04 + 2.0 * 0.08 + 0.03 + 0.0115 + 0.04 + 0.2 + 0.03 + 0.0115 + 0.04 + 0.2,
                   relwidth=0.15, 
                   relheight=0.03)
        self.create_widget(parent)

    def create_widget(self, parent):
        """
        Create header label, automation button, and progress bar.
        """

        # Run Automation button
        btn_run = tk.Button(self, text="Run Predictions",
                            font=("Segoe UI", 10),
                            relief="solid", bd=1,
                            highlightthickness=1,
                            padx=20, pady=0,
                            height=1,
                            command=lambda: self.run_automation(parent))

        # Progress bar
        self.progress_bar = ttk.Progressbar(self, orient="horizontal",
                                            mode="determinate", maximum=100)
        #self.progress_bar.pack(fill="x", padx=10, pady=(5, 0))
        
        btn_run.pack(side='left', anchor='e', expand=True, fill='both')
        self.progress_bar.pack(side='right', anchor='w', expand=True, fill='both')
        

    def run_automation(self, parent):
        """
        Run RF model predictions on all images and save outputs.
        """
        if not hasattr(parent, 'RFmodel') or parent.RFmodel is None:
            print("⚠️ No trained Random Forest model found. Train model first.")
            return

        # Create prediction output folder
        prediction_folder = Path(parent.filedirectory) / "output" / "prediction"
        prediction_folder.mkdir(parents=True, exist_ok=True)

        # Get selected filenames if the tkinter boolean is true
        selected_filenames = [img_path for img_path, var in parent.image_vars if var.get()]
        
        # Check if any images are selected
        if len(selected_filenames) == 0:
            print("⚠️ No images selected, please choose between 'select All' or 'Every 2nd' in the Automation Manager")
            return
                   
        # Get the length of the selected images
        total_images = len(selected_filenames)
        print(f"📂 Predictions will be saved in: {prediction_folder}")

        # Run through the selected images
        for idx, img_path in enumerate(selected_filenames):
            
            # Get image names
            img_name = Path(img_path).stem
            
            # Create numpy and png extension for saving
            pred_npy = prediction_folder / f"{img_name}_pred.npy"
            pred_png = prediction_folder / f"{img_name}_pred.png"
            
            # Print progression
            print(f"🔄 Processing {img_name} ({idx + 1}/{total_images})")

            # Load image and convert to RGBA if necessary
            img_rgb = ensure_rgba(img_path)
            img_gra = img_rgb.convert("L")
            
            # preprocess for random-forest -> grayscale -> numpy array 
            img_array = np.array(img_rgb.convert("L"))

            # Get features
            features = parent.feature_selector.get_selected_features()

            # Predict features onto image
            img_prediction = predict_features(parent.RFmodel, img_array, features)

            # Predict
            prediction_mask = img_prediction.reshape(img_array.shape)

            # Save .npy
            np.save(pred_npy, prediction_mask)

            # Save color overlay as PNG
            img_rgb = np.array(img_rgb)
            for label_idx, rgb in enumerate(parent.lab_color_rgb, start=1):
                img_rgb[prediction_mask == label_idx, :3] = rgb
            overlay_pil = PIL.Image.fromarray(img_rgb, mode="RGBA")
            overlay_pil.save(pred_png)

            print(f"✅ Saved: {pred_npy.name}, {pred_png.name}")

            # Update progress bar
            progress = ((idx + 1) / total_images) * 100
            self.progress_bar['value'] = progress
            parent.update_idletasks()

        print("🎉 Automation completed successfully!")
        self.progress_bar['value'] = 100  # Complete
