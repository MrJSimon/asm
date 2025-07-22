"""Develop buttons to paint the image segments and exporting the trained images"""
import os
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np


class PaintToolsText(ttk.Frame):
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
        self.place(relx=0.165, rely=0.095, relwidth=0.15,
                   relheight=0.04)
        self.create_widget(parent)

    def create_widget(self,parent):
        """Create and configure the label for the RF classifier.

        Args:
            parent: The parent widget in which the label is placed.
        """
        #HEADER TITLE
        l = ttk.Label(self, text="🎨 Paint tools", 
              font=('Times', 24), anchor="w", justify="left")
        l.grid(row=0, column=0, sticky='w', padx=5, pady=(5, 10))



class DrawingTools(ttk.Frame):
    """A frame widget that provides drawing tools like paint, erase, and lasso.

    Attributes:
        parent: The parent widget in which this frame is placed.
    """

    def __init__(self, parent):
        """Initialize the frame and place it within the parent widget.

        Args:
            parent: The parent widget in which this frame is placed.
        """
        super().__init__(parent)
        self.place(relx=0.165, rely=0.095+0.04, relwidth=0.15, relheight=0.04)
        self.create_widget(parent)

    def create_widget(self, parent):
        """Create and configure the drawing tool buttons.

        Args:
            parent: The parent widget in which the buttons are placed.
        """
        # Create buttons
        b_paint = tk.Button(self,  
                            text='🖌️', 
                            font=("Segoe UI", 24),
                            relief="solid", bd=1,  # Solid border
                            highlightthickness=1,
                            padx=20, pady=0,       # Reduce vertical padding
                            height=1,       
                            command=lambda: self.paint_1(parent))
        b_erase = tk.Button(self, 
                             text='🧽', 
                             font=("Segoe UI", 24),
                             relief="solid", bd=1,  # Solid border
                             highlightthickness=1,
                             padx=20, pady=0,       # Reduce vertical padding
                             height=1,                               
                             command=lambda: self.paint_2(parent))
        # Position buttons
        b_paint.pack(side='left', anchor='e', expand=True, fill='both')
        b_erase.pack(side='right', anchor='w', expand=True, fill='both')        

    def paint_1(self, parent):
        """Toggle the paint mode on or off.

        Args:
            parent: The parent widget that holds the mode states.
        """
        #print('Inside paint 1')
        if parent.paint_mode != 'activated':
            parent.paint_mode = 'activated'
            parent.erase_mode = 'deactivated'
        else:
            parent.paint_mode = 'deactivated'

    @staticmethod
    def paint_2(parent):
        """Toggle the erase mode on or off.

        Args:
            parent: The parent widget that holds the mode states.
        """
        print('Inside paint 2')
        if parent.erase_mode != 'activated':
            parent.erase_mode = 'activated'
            parent.paint_mode = 'deactivated'
        else:
            parent.erase_mode = 'deactivated'

class ScrollTools(ttk.Frame):
    """A frame widget that provides a slider tool for adjusting brush size."""

    def __init__(self, parent):
        """Initialize the frame and place it within the parent widget."""
        super().__init__(parent, borderwidth=1, relief="solid")
        self.place(relx=0.165, rely=0.095+0.04+0.04,
                   relwidth=0.15, relheight=0.06)  # slightly taller
        self.create_widget(parent)

    def create_widget(self, parent):
        """Create and configure the slider for brush size adjustment."""

        # Frame to hold small-to-large circle labels
        indicator_frame = ttk.Frame(self)
        indicator_frame.pack(side=tk.TOP, fill=tk.X, padx=2, pady=(2, 0))

        # Add small-to-large circle indicators as labels
        num_circles = 5
        min_size = 6   # font size for smallest dot
        max_size = 30  # font size for largest dot
        for i in range(num_circles):
            size = min_size + (max_size - min_size) * (i / (num_circles - 1))
            lbl = ttk.Label(indicator_frame, text="●", foreground="gray")
            lbl.pack(side=tk.LEFT, expand=True)
            lbl.configure(font=("TkDefaultFont", int(size)))

        # Create the scale slider below the indicators
        self.block_paint_slider = ttk.Scale(
            self,
            from_=1,
            to=100,
            orient=tk.HORIZONTAL,
            command=lambda i: self.slider_command(i, parent)
        )
        self.block_paint_slider.set(5)
        self.block_paint_slider.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=(0, 2))

    @staticmethod
    def slider_command(i, parent):
        """Adjust the brush size based on the slider's position."""
        parent.mouse_s = int(float(i))


# class ScrollTools(ttk.Frame):
#     """A frame widget that provides a slider tool for adjusting brush size.

#     Attributes:
#         parent: The parent widget in which this frame is placed.
#     """

#     def __init__(self, parent):
#         """Initialize the frame and place it within the parent widget.

#         Args:
#             parent: The parent widget in which this frame is placed.
#         """
#         super().__init__(parent, borderwidth=1, relief="solid")
#         self.place(relx=0.320 - 0.035, rely=0.01+0.04+0.04, relwidth=0.15,
#                    relheight=0.04)
#         self.create_widget(parent)

#     def create_widget(self, parent):
#         """Create and configure the slider for brush size adjustment.

#         Args:
#             parent: The parent widget that holds the brush size state.
#         """
#         block_paint_slider = ttk.Scale(
#             self,
#             from_=0,
#             to=255,
#             orient=tk.HORIZONTAL,
#             variable=tk.IntVar,
#             command=lambda i: self.slider_command(i, parent)
#         )
#         block_paint_slider.set(5)
#         block_paint_slider.pack(expand=True, fill='both')

#     @staticmethod
#     def slider_command(i, parent):
#         """Adjust the brush size based on the slider's position.

#         Args:
#             i: The current position of the slider.
#             parent: The parent widget that holds the brush size state.
#         """
#         parent.mouse_s = int(float(i))


class ExportImage(ttk.Frame):
    """A frame widget for exporting mask and image data.

    Attributes:
        parent: The parent widget in which this frame is placed.
    """

    def __init__(self, parent):
        """Initialize the frame and place it within the parent widget.

        Args:
            parent: The parent widget in which this frame is placed.
        """
        super().__init__(parent)
        self.place(relx=0.320 - 0.035, rely=0.55, relwidth=0.035,
                   relheight=0.05)
        self.create_widget(parent)

    def create_widget(self, parent):
        """Create and configure the export button.

        Args:
            parent: The parent widget in which the button is placed.
        """
        # Create buttons
        be = ttk.Button(self, text='exp.',
                        command=lambda: self.export_button(parent))
        # Position buttons
        be.pack(expand=True, fill='both')

    @staticmethod
    def export_button(parent):
        """Export mask and image data to files and display the mask image.

        Args:
        parent: The parent widget containing image data and file paths.
        """
        print('Saving mask and image data')

        # Define the base output directory
        output_dir = 'output'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Define subdirectories for masks, images, and figures
        mask_dir = os.path.join(output_dir, 'masks')
        img_dir = os.path.join(output_dir, 'images')
        fig_dir = os.path.join(output_dir, 'figures')

        # Create subdirectories if they don't exist
        for subdir in [mask_dir, img_dir, fig_dir]:
            if not os.path.exists(subdir):
             os.makedirs(subdir)

        # Save the mask and image data to their respective subdirectories
        mask_path = os.path.join(mask_dir, 'mask_' + str(parent.img_numb) + '.txt')
        img_path = os.path.join(img_dir, 'img_' + str(parent.img_numb) + '.txt')
        np.savetxt(mask_path, parent.img_j)
        np.savetxt(img_path, parent.img_i)

        # Display and save the figure in the figures subdirectory
        fig_path = os.path.join(fig_dir, 'figure_' + str(parent.img_numb) + '.png')
        plt.figure()
        plt.imshow(parent.img_j)
        plt.savefig(fig_path, bbox_inches='tight')
        plt.show()
        print('Files saved:', mask_path, img_path, fig_path)