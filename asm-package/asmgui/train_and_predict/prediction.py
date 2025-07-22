"""The module trains the segmented images and predict images based on trained 
    data using random forest classifier"""
from tkinter import ttk
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from ..randomforest_classifier.training_functions import predict_features
from ..randomforest_classifier.training_functions import train_random_forest
from ..image_analysis.image_analysis_tools import ensure_rgba
import PIL.Image
import json
from pathlib import Path
from tkinter import filedialog

class ClassifierText(ttk.Frame):
    """A frame widget that displays a label for the RF classifier.

    Attributes:
        parent: The parent widget in which this frame is placed.
    """

    def __init__(self, parent):
        """Initialize the frame and place it within the parent widget.

        Args:
            parent: The parent widget in which this frame is placed.
        """
        #super().__init__(parent,borderwidth=2, relief="solid")
        #self.place(x=5.0, rely=0.095, relwidth=0.15, relheight=0.04)
        #self.create_widget(parent)
        
        super().__init__(parent,borderwidth=2, relief="solid")
        self.place(x=5.0, rely=0.095 + 0.04+2.0*0.08+0.03+0.0115, relwidth=0.15,
                   relheight=0.04)
        self.create_widget(parent)

    def create_widget(self,parent):
        """Create and configure the label for the RF classifier.

        Args:
            parent: The parent widget in which the label is placed.
        """
        #HEADER TITLE
        l = ttk.Label(self, text="🌲 Random Forest Classifier", 
              font=('Times', 24), anchor="w", justify="left")
        l.grid(row=0, column=0, sticky='w', padx=5, pady=(5, 10))

class FeatureSelector(tk.Frame):
    """
    Frame widget for selecting image features for ASM application.
    """
    def __init__(self, parent):
        """
        Initialize FeatureSelector frame.

        Args:
            parent: The parent widget.
        """
        super().__init__(parent, borderwidth=1, relief="solid")
        # Position in parent window
        self.place(x=5.0, rely=0.095 + 0.04 + 2.0 * 0.08 + 0.03 + 0.0115 + 0.04,
                   relwidth=0.15, relheight=0.2)  # increased relheight for more content
        self.create_widget(parent)

    def create_widget(self, parent):
        """
        Create label and checkboxes for feature selection.

        Args:
            parent: The parent widget.
        """
        # Section label
        l = ttk.Label(self, text="Select Features:", 
                      font=('Times', 10, 'bold'), anchor="w", justify="left")
        l.grid(row=0, column=0, sticky='w', padx=2, pady=(2, 5))

        # Features list
        self.features = parent.features
        self.feature_vars = {}  # Holds BooleanVars for each feature

        # Create checkboxes for each feature
        for i, feature in enumerate(self.features, start=1):
            var = tk.BooleanVar(value=True)  # Default: selected
            cb = ttk.Checkbutton(self, text=feature, variable=var)
            cb.grid(row=i, column=0, sticky='w', padx=5, pady=1)
            self.feature_vars[feature] = var

    def get_selected_features(self):
        """
        Return a list of selected features.
        """
        return [f for f, v in self.feature_vars.items() if v.get()]

class ClassifierButtons(ttk.Frame):
    """A frame widget that provides buttons for training and predicting with a classifier.

    Attributes:
        parent: The parent widget in which this frame is placed.
    """

    def __init__(self, parent):
        """Initialize the frame and place it within the parent widget.

        Args:
            parent: The parent widget in which this frame is placed.
        """
        super().__init__(parent)
        self.place(x=5.0, rely=0.095 + 0.04+2.0*0.08+0.03+0.0115+0.04+0.2, 
                   relwidth=0.15,relheight=0.03)
        self.create_widget(parent)

    def create_widget(self, parent):
        """Create and configure the training and predicting buttons.

        Args:
            parent: The parent widget in which the buttons are placed.
        """
        # Create buttons
        bt = tk.Button(self, text='train', 
                        font=("Segoe UI", 10),
                        relief="solid", bd=1,  # Solid border
                        highlightthickness=1,
                        padx=20, pady=0,       # Reduce vertical padding
                        height=1,                        
                        command=lambda: self.train(parent))
        bp = tk.Button(self, text='predict', 
                        font=("Segoe UI", 10),
                        relief="solid", bd=1,  # Solid border
                        highlightthickness=1,
                        padx=20, pady=0,       # Reduce vertical padding
                        height=1,
                        command=lambda: self.predict(parent))
        # Position buttons
        bt.pack(side='left', anchor='e', expand=True, fill='both')
        bp.pack(side='right', anchor='w', expand=True, fill='both')

    @staticmethod
    def train(parent):
        """Train a random forest decision tree on the image data.

        Args:
            parent: The parent widget containing the image data and model list.
        """
        print('Training random forest decision tree on image')
        
        ## Initiate lists
        image_list = []
        masks_list = []
        
        ## run through image paths
        for img_path in parent.training_image_paths:
            ## Get original image
            orig_image = ensure_rgba(img_path).convert("L")
            orig_array = np.array(orig_image)
            ## Filename and path
            mask_filename = Path(img_path).stem + "_mask.npy"
            mask_path = Path(parent.filedirectory) / "output" / "masks" / mask_filename
            ## Get corresponding mask
            mask_array = np.load(mask_path)
            ## Append to list's 
            image_list.append(orig_array)
            masks_list.append(mask_array)
        
        # Merge images and train the model
        img_fj = np.concatenate(image_list,axis=1)
        img_mj = np.concatenate(masks_list,axis=1)     
        # Get selected features
        features = parent.feature_selector.get_selected_features()
        print("Selected Features:", features) ## WE NEED TO GET THE FEATURES HERE
        # Train model
        model = train_random_forest(img_mj,img_fj,features)
        # Append model to parent main
        parent.RFmodel = model
        print('training finished')
        #🆕 Refresh Training Set Manager to show new image
        if hasattr(parent, 'training_set_manager'):
            parent.training_set_manager.refresh()

    @staticmethod
    def predict(parent):
        """Predict features onto the image using the trained model.

        Args:
            parent: The parent widget containing the trained model and image data.
        """
        print('predicting stuff')
        
        # Get the new image
        #img_filename = parent.img_filenames[parent.img_numb]
        
        #parent.image_c = PIL.Image.open(img_filename)
        
        #parent.image_c = ensure_rgba(img_filename)
        
        ## Convert the unomodified pil-image into graysacel 2D numpy array
        img_i = np.array(parent.image_c.convert("L"))       
        # Get selected features
        features = parent.feature_selector.get_selected_features()     
        # Predict features onto image
        img_j = predict_features(parent.RFmodel,img_i,features)
        # Show images
        f, (ax1, ax2) = plt.subplots(1,2,sharey=True)
        ax1.imshow(img_i)
        ax2.imshow(img_j)
        plt.tight_layout()
        plt.show()
        print('prediction finished')


class TrainingSetManagerText(ttk.Frame):
    """A frame widget that displays a label for the RF classifier.

    Attributes:
        parent: The parent widget in which this frame is placed.
    """

    def __init__(self, parent):
        """
        Initialize TrainingSetManager frame.

        Args:
            parent: The parent widget.
        """
        super().__init__(parent, borderwidth=1, relief="solid")
        self.place(
            x=5.0,
            rely=0.095 + 0.04 + 2.0 * 0.08 + 0.03 + 0.0115 + 0.04 + 0.2 + 0.03 + 0.0115,
            relwidth=0.15,
            relheight=0.04  # Adjust for how many thumbnails to show
        )
        self.parent = parent
        self.create_widget()

    def create_widget(self):
        """
        Create scrollable area displaying trained images with remove buttons.
        """
        # Section label
        #HEADER TITLE
        l = ttk.Label(self, text="🖼️ Masking Manager", 
              font=('Times', 24), anchor="w", justify="left")
        l.grid(row=0, column=0, sticky='w', padx=5, pady=(5, 10))

          
class TrainingSetManager(tk.Frame):
    """
    Frame widget embedded in the main window for managing training dataset.
    Displays thumbnails of all trained images and allows removal.
    """
    def __init__(self, parent):
        """
        Initialize TrainingSetManager frame.

        Args:
            parent: The parent widget.
        """
        super().__init__(parent, borderwidth=1, relief="solid")
        self.place(
            x=5.0,
            rely=0.095 + 0.04 + 2.0 * 0.08 + 0.03 + 0.0115 + 0.04 + 0.2 + 0.03 + 0.0115 + 0.04,
            relwidth=0.15,
            relheight=0.2  # Adjust for how many thumbnails to show
        )
        self.parent = parent
        self.create_widget()

    def create_widget(self):
        """
        Create scrollable area displaying trained images with remove buttons.
        """

        # Scrollable canvas
        canvas = tk.Canvas(self, borderwidth=0, background="#f0f0f0")
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas, background="#f0f0f0")

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.refresh()

    def refresh(self):
        """
        Refresh the thumbnails and buttons in a 3-column grid layout.
        """
        # Clear any existing widgets
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
    
        # Make 3 columns expand equally
        for c in range(3):
            self.scroll_frame.grid_columnconfigure(c, weight=1)
    
        # Loop through training_image_paths and training_mask_paths together
        for idx, (img_path, mask_path) in enumerate(
            zip(self.parent.training_image_paths, self.parent.training_mask_paths)
        ):
            # Load original image
            orig_img = ensure_rgba(img_path)
            #orig_img = PIL.Image.open(img_path).convert("RGBA")
            img_array = np.array(orig_img)
    
            # Load corresponding mask
            mask_array = np.load(mask_path)
    
            # Replace RGB values at mask indices with corresponding colors
            for label_idx, rgb in enumerate(self.parent.lab_color_rgb, start=1):
                img_array[mask_array == label_idx, :3] = rgb  # Replace RGB channels only
    
            # Convert back to PIL after NumPy modification
            combined = PIL.Image.fromarray(img_array, mode="RGBA")
    
            # Create thumbnail
            thumbnail = combined.copy()
            thumbnail.thumbnail((120, 120))
            tk_thumb = PIL.ImageTk.PhotoImage(thumbnail)
    
            # Create frame for thumbnail + remove button
            frame = tk.Frame(self.scroll_frame, bd=1, relief="solid", background="#ffffff")
            label = tk.Label(frame, image=tk_thumb)
            label.image = tk_thumb  # Prevent garbage collection
            label.pack()
    
            btn_remove = tk.Button(
                frame, text="Remove", font=("Segoe UI", 8),
                command=lambda p=img_path, m=mask_path: self.remove_image(p, m)
            )
            btn_remove.pack(fill="x")
    
            # Place frame in 3-column grid
            row = idx // 3
            col = idx % 3
            frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")



    def remove_image(self, img_path, mask_path):
        """
        Remove an image and its mask from training set and disk.
        """
        print(f"Removing {img_path} and {mask_path}")
    
        # Remove paths from parent lists
        if img_path in self.parent.training_image_paths:
            self.parent.training_image_paths.remove(img_path)
        if mask_path in self.parent.training_mask_paths:
            self.parent.training_mask_paths.remove(mask_path)
    
        # Delete mask file from disk
        mask_file = Path(mask_path)
        if mask_file.exists():
            mask_file.unlink()
            print(f"Deleted mask file: {mask_file.name}")
    
        # Save updated JSON
        if hasattr(self.parent, "save_training_set"):
            self.parent.save_training_set(self.parent)
    
        # Refresh UI
        self.refresh()
        # Refresh image window
        #self.parent.image_window()
        

class SaveLoadJSON(ttk.Frame):
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
        bp = tk.Button(self, text='load json',
                       font=("Segoe UI", 10),
                       relief="solid", bd=1,
                       highlightthickness=1,
                       padx=20, pady=0,
                       height=1,
                       command=lambda: self.load_training_set(parent))

        bt.pack(side='left', anchor='e', expand=True, fill='both')
        bp.pack(side='right', anchor='w', expand=True, fill='both')

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
        data = {
            "images": parent.training_image_paths,
            "masks": parent.training_mask_paths,
            "features": parent.feature_selector.get_selected_features()
        }
    
        # Save JSON
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Training set saved to {filepath}")

    @staticmethod
    def load_training_set(parent, filepath=None):
        """
        Load training set from JSON file and rebuild Random Forest model.
        If no filepath is given, prompt user to select one.
        """
        # Prompt user if no filepath provided
        if filepath is None:
            json_file = filedialog.askopenfilename(
                title="Select Training Set JSON",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if not json_file:
                print("Load canceled: no file selected.")
                return  # User canceled
            filepath = Path(json_file).resolve()
        else:
            filepath = Path(filepath).resolve()
    
        print(f"Loading training set from {filepath}")
    
        # Load JSON data
        with open(filepath, 'r') as f:
            data = json.load(f)
    
        # Restore paths
        parent.training_image_paths = data.get("images", [])
        parent.training_mask_paths = data.get("masks", [])
    
        # Get features
        selected_features = data.get("features", [])
    
        # Restore selected features in GUI
        print("Restoring selected features:", selected_features)
        for feature, var in parent.feature_selector.feature_vars.items():
            var.set(feature in selected_features)
    
        print(f"Training set loaded from {filepath}")
    
        # Refresh UI if Training Set Manager exists
        if hasattr(parent, 'training_set_manager'):
            parent.training_set_manager.refresh()

