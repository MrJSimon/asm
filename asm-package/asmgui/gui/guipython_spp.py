"""Main GUI setup"""
import tkinter as tk
import numpy as np
import PIL
from ..load_images.image_loader import ImageLoader
from ..load_images.json_loader import JsonLoader, JsonSaver
from ..window_manager.status_manager import StatusManager, LabelManagerText
from ..window_manager.status_manager import LabelManagerPmButtons, LabelManagerLabels
from ..image_window.main_image_window import ImageWindow, ImageWindowPmButtons
from ..draw_and_export.drawing_tools import DrawingTools, ScrollTools, PaintToolsText
from ..draw_and_export.drawing_tools import ExportImage
from ..train_and_predict.prediction import ClassifierText, ClassifierButtons, FeatureSelector, TrainingSetManager, TrainingSetManagerText#, SaveLoadJSON
from ..train_and_predict.automation import AutomationManager, AutomationManagerText, AutomationImageSelector
#from ..draw_and_export.drawing_tools import zoomtools

# Define class
class ASM(tk.Tk):
    """
    ASM (Automated segmentation manager) GUI application for image 
    annotation and analysis.

    Attributes:
        title (str): Title of the ASM application window.
        image_loader (ImageLoader): Widget for loading images.
        status_manager (StatusManager): Widget for managing status.
        label_manager_text (LabelManagerText): Widget for managing text labels.
        label_manager_pmbuttons (LabelManagerPmButtons): Widget for managing label buttons.
        label_manager_labels (LabelManagerLabels): Widget for managing labels.
        image_window (ImageWindow): Widget for displaying images.
        image_window_pmbuttons (ImageWindowPmButtons): Widget for managing image window buttons.
        drawing_tools (DrawingTools): Widget for drawing tools.
        scroll_tools (ScrollTools): Widget for scrolling tools.
        export_image (ExportImage): Widget for exporting images.
        classifier_text (ClassifierText): Widget for classifying text.
        classifier_buttons (ClassifierButtons): Widget for classifier buttons. 
    """

    def __init__(self, title):
        """
        Initialize ASM GUI application.

        Args:
            title (str): The title for the main window.
        """
        # Main setup
        super().__init__()
        self.title(title)
        self.state('zoomed')
        self.configure(bg="aliceblue")

        # Create list with images and names
        self.img_filenames = []
        self.img_mask = []
        self.img_list = []
        self.img_name = []
        self.lab_name = []
        self.list_m = []
        self.list_f = []
        self.lab_acti = "none"
        self.lab_color_rgb = [(0,0,255),(76,169,65),(255,0,0),(255,255,0),(0,255,255),(255,0,255)]
        self.img_numb = 0
        self.img_i = PIL.Image.new("RGB", (500, 500), (0, 0, 0))
        self.img_j = PIL.Image.new("RGB", (500, 500), (0, 0, 0))
        self.image_c = PIL.Image.new("RGB", (500, 500), (0, 0, 0))
        self.image_f = PIL.Image.new("RGB", (500, 500), (0, 0, 0))
        self.image_m = PIL.Image.new("L", self.image_c.size, 0)
        #self.img_i = np.zeros([500, 500])
        #self.img_j = np.zeros([500, 500])
        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_s = 5
        self.paint_mode = "deactivated"
        self.erase_mode = "deactivated"
        self.lasso_mode = "deactivated"
        self.zoom_mode  = "deactivated"
        
        self.features = [
            'denoise', 'Laplacian', 'Canny Edge', 'Sobel', 'Scharr',
            'Prewitt', 'Gaussian σ=3', 'Gaussian σ=7', 'Median size=3'
        ]
        
        self.filedirectory = ''
        self.predict_image_paths = []
        self.training_image_paths = []
        self.training_mask_paths = []
        self.current_image_path = ''
        self.image_vars = []

        # Initialize Widgets
        # Widget - Image loader
        self.image_loader = ImageLoader(self)
        self.json_loader  = JsonLoader(self)
        # Widget - Status manager
        #self.status_manager = StatusManager(self)

        # Widget - Label manager
        self.label_manager_text = LabelManagerText(self)
        self.label_manager_pmbuttons = LabelManagerPmButtons(self)
        self.label_manager_labels = LabelManagerLabels(self)

        # Widget - Image window
        self.image_window = ImageWindow(self)
        self.image_window_pmbuttons = ImageWindowPmButtons(self)
        # Widget - Drawing tools
        self.drawing_tools_text = PaintToolsText(self)
        self.drawing_tools = DrawingTools(self)

        # Widget - Scrolling tools
        self.scroll_tools = ScrollTools(self)

        # Widget - Export image
        #self.export_image = ExportImage(self)
        
        # Widget - Classifier
        self.classifier_text = ClassifierText(self)
        self.feature_selector = FeatureSelector(self)
        self.classifier_buttons = ClassifierButtons(self)
        self.training_set_manager_text = TrainingSetManagerText(self)
        self.training_set_manager = TrainingSetManager(self)
        self.save_load_json = JsonSaver(self)
        
        # Widget - AutomationManager
        self.automation_manager_text = AutomationManagerText(self)
        self.automation_image_selector = AutomationImageSelector(self)
        self.automation_manager = AutomationManager(self)


        self.mainloop()
        