# asm
**asm** is an assisted 2D image segmentation tool built with Python. It employs a Random Forest classifier for pixel-wise segmentation and provides a full-featured GUI for semi-automated workflows.

# Purpose
ASM is designed for researchers and practitioners working in fields that utilize microscopy, scanning electron microscopy (SEM), and X-Ray imaging, where precise and efficient 2D segmentation is critical.

1. Quickly load and manage image datasets
2. Create, edit, and organize training masks
3. Extract and select features for classification
4. Train Random Forest models and apply them to unseen images
5. Visualize predictions and overlay segmentations

# Installation
Install **asm** by cloning the repository onto your local machine using the following command

    git clone https://github.com/yourusername/asm.git

## Requirements

This program was tested using

    python 3.10.9

Install the required Python packages, listed in requirements.txt, with:  

    pip install -r requirements.txt

# Getting started
This package can be executed from a Python IDE (e.g., PyCharm, VSCode, Spyder) or via the terminal. 

To start the GUI, navigate to the asm package and run:

    python asm\asm-package\start_GUI.py

# Basic workflow
The workflow is designed to guide users from data loading to model training and prediction:

### 📂 Step 1: Load Images
Use the **Image Loader** to select and load the directory containing your images. Supported formats include `.png`, `.jpg`, `.tif`, and `.bmp`.

### 🔖 Step 2: Label Manager
Use the plus/+ or minus/- sign to add or remove labels. The program currently supports 9 labels.

### 🎨 Step 3: Paint tools
To mask an image start by:

&nbsp;&nbsp;&nbsp;&nbsp; **3.1** Activate the label of interest by pressing the added label-button  
&nbsp;&nbsp;&nbsp;&nbsp; **3.2** Press the brush tool button  
&nbsp;&nbsp;&nbsp;&nbsp; **3.3** Guide the mouse to the main image window and paint on top of the image 

Please note: ⚠️ The brush and eraser tool will only work on the image, not on the entire canvas.

### 📊 Step 3: Select Features
In the **Random Forest Classifier** panel, choose the features to include in training (e.g., Sobel, Canny Edge, Gaussian filters).

### 🌲 Step 4: Random Forest Classifier
Click **Train** to build a Random Forest model using the selected features and masks.

### 🔮 Step 5: Predict Segmentation
Use the **Predict** button to apply the trained model to the image shown in the main GUI window. 

Predictions will appear in a **separate** window next to the original image.

### 🤖 Step 5: Automation Manager
To apply the trained model to multiple images:

&nbsp;&nbsp;&nbsp;&nbsp; 5.1 Use the **Automation Manager** to select or deselect the images to be predicted  
&nbsp;&nbsp;&nbsp;&nbsp; 5.2 Press the **Predict** button to apply the trained model to the selected images  
&nbsp;&nbsp;&nbsp;&nbsp; 5.3 Lean back and relax while ASM processes the batch

### 📝 Step 6: Save Results
Save prediction outputs and updated masks for further analysis using a .json file




# Visualizations


# Output Files

| File Name                               | Description                                |
|-----------------------------------------|--------------------------------------------|
| ................................        | ...............................            |


# Documentation
For more details, visit the Wiki (if any)
