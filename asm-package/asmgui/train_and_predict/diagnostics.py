# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 06:47:53 2025

@author: jeg_e
"""
## Load in packages
from tkinter import ttk
import tkinter as tk
import numpy as np
from ..randomforest_classifier.training_functions import predict_features
import PIL.Image
from pathlib import Path
from ..image_analysis.image_analysis_tools import ensure_rgba

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class DiagnosticsText(ttk.Frame):
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
                   rely=0.095 + 0.04+2.0*0.08+0.03+0.0115,
                   relwidth=0.15, relheight=0.04)
        self.create_widget(parent)

    def create_widget(self, parent):
        """
        Create and configure the label widget.

        Args:
            parent: The parent widget.
        """
        #HEADER TITLE
        l = ttk.Label(self, text="\U0001F4CA Diagnostics Manager", 
              font=('Times', 24), anchor="w", justify="left")
        l.grid(row=0, column=0, sticky='w', padx=5, pady=(5, 10))
        
    
class PiechartClassifier(ttk.Frame):
    """
    A frame widget for selecting which images to run predictions on.
    """
    def __init__(self, parent):
        super().__init__(parent, borderwidth=0, relief="solid")
        
        self.place(relx=0.165,
                   rely=0.095 + 0.04+2.0*0.08+0.03+0.0115+0.04,
                   relwidth=0.15, relheight=0.2)
              
        self.create_widget(parent)

    def create_widget(self, parent):
        
    
        # Create dummy-pie with 100 %
        pie_name = ['No data yet']
        pie_value = [100]
        
        # Create figure to self
        self.fig = Figure(figsize=(2, 2), dpi=100)
        
        # Get axes from figure
        self.ax = self.fig.add_subplot(111)
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        
        # Create pie
        self.ax.pie(pie_value,radius=1.25,labels=pie_name,autopct='%0.1f%%',shadow=False)
        
        ## Make widget expand entire widget
        self.canvas.get_tk_widget().pack(expand=True, fill="both")

        # placeholder content
        self.canvas.draw()
        
        
    
        
    def update_from_model(self, parent):
        # Selected feature names (same order as the model’s features)
        feature_names = parent.feature_selector.get_selected_features()
    
        # Mean importances across trees
        importances = parent.RFmodel.feature_importances_
    
        # Std across trees
        std = np.std([t.feature_importances_ for t in parent.RFmodel.estimators_], axis=0)
    
        # Normalize both mean and std by the same sum so percentages match the pie
        S = importances.sum() or 1.0
        vals = importances / S
        std_norm = std / S
    
        # Put the ±std% into the labels; autopct still prints mean %
        labels = [f"{name}\n±{std_norm[i]*100:.1f}%"
                  for i, name in enumerate(feature_names)]
    
        self.ax.clear()
        self.ax.pie(
            vals,
            labels=labels,
            autopct="%0.1f%%",   # mean %
            startangle=90,
            shadow=False,
        )
        self.fig.tight_layout()
        self.canvas.draw_idle()
        
        
    #     # Get selected features
    #     feature_names = parent.feature_selector.get_selected_features()

    #     # Get mean feature values across treesss 
    #     importances = parent.RFmodel.feature_importances_
        
    #     # Normalize
    #     importances = importances / importances.sum()
        
    #     self.ax.clear()
    #     self.ax.pie(
    #         importances,
    #         labels=feature_names,
    #         autopct="%0.1f%%",
    #         startangle=90,
    #         shadow=False,
    #     )
    #     self.fig.tight_layout()
    #     self.canvas.draw_idle()
        
    #     # #feature_names = getattr(parent, "feature_names",
    #     #                        [f"F{i}" for i in range(len(importances))])
