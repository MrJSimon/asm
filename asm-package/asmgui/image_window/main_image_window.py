"""This module represent the main image window frame"""
import tkinter as tk
from tkinter import ttk
import PIL.Image
import PIL.ImageTk
import PIL.Image
import PIL.ImageDraw
import PIL
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from ..image_analysis.image_analysis_tools import ensure_rgba

class ImageWindow(tk.Frame):
    """
    A frame widget for displaying images in the ASM application.

    Attributes:
        parent (tk.Tk): The parent window.
    """

    def __init__(self, parent):
        """
        Initialize ImageWindow frame and place it within the parent widget.

        Args:
            parent: The parent widget.
        """
        super().__init__(parent)
        self.place(relx=0.320, y=5, relwidth=0.67, relheight=0.90)
        self.create_widget(parent)


    def create_widget(self, parent):
        '''
        Create initial widgets including a fake image, scrollbars, and canvas.

        Args:
            parent: The parent widget that contains the image and other properties.
        '''
        ## Create initial fake image
        #img_i = np.copy(parent.img_i)

        ## Set horizontal and vertical scrollbar
        vbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        hbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        
        ## Create canvas
        self.canvas = tk.Canvas(self,bg="white",highlightthickness=0,xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        
        ## Pack the horizontal and vertical bar onto
        hbar.pack(side=tk.BOTTOM, fill=tk.X)
        vbar.pack(side=tk.RIGHT,  fill=tk.Y)
        
        ## Expand the pack
        self.canvas.pack(expand=True, fill='both')

        ## Update canvas
        self.canvas.update()

        ## Configure the scrolls
        vbar.configure(command=self.scroll_y)  # bind scrollbars to the canvas
        hbar.configure(command=self.scroll_x)
        
        # Make the canvas expandable
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        
        ###################### keep this ###############################
        #parent.image_c = parent.img_i.copy()    
        #parent.image_f = parent.img_i.copy()
        #parent.image_m = PIL.Image.new("L", parent.img_i.size, 0)
        

        def interhandler(event):
            """Intermediate handler to pass the parent object into event functions."""
            return self.get_xy_position(event, parent)

        # Bind events to the Canvas
        self.canvas.bind('<Configure>', self.show_image)  # canvas is resized
        #self.canvas.bind('<ButtonPress-1>', self.move_from)
        #self.canvas.bind('<B1-Motion>',     self.move_to)
        self.canvas.bind('<MouseWheel>', self.wheel)  # with Windows and MacOS, but not Linux
        self.canvas.bind('<Button-5>',   self.wheel)  # only with Linux, wheel scroll down
        self.canvas.bind('<Button-4>',   self.wheel)  # only with Linux, wheel scroll up
        self.canvas.bind("<Button-1>", interhandler)
        self.canvas.bind("<B1-Motion>", lambda event, parent=parent: self.draw_smth(event,parent))
        
        
        ## Set scale value for canvas image and zoom magnitude
        self.imscale, self.delta = 1.0, 1.3
        
        ## Convert to pil-image 
        #self.image = PIL.Image.fromarray(parent.image_f).convert("RGB")
        #self.image = parent.image_f.copy()
        
        
        ## Set width and height of image
        #self.width, self.height = self.image.size[0], self.image.size[1]
        
        ## Compute the offset
        #offset = self.computeoffset(self.canvas.winfo_height(),
        #                            self.canvas.winfo_width(),
        #                            self.height,self.width)
        
        ## Set container.
        #self.container = self.canvas.create_rectangle(offset[0], offset[1], self.width+offset[0], self.height+offset[1])
        
        ## Show image has to be initialized here otherwize
        #self.show_image(self.canvas.winfo_height(),self.canvas.winfo_height())
        
        self.refresh_from_parent(parent)
        

    def computeoffset(self,bg_h,bg_w,img_h,img_w):
        offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
        return offset

    def scroll_y(self, *args, **kwargs):
        ''' Scroll canvas vertically and redraw the image '''
        self.canvas.yview(*args, **kwargs)  # scroll vertically
        self.show_image()  # redraw the image

    def scroll_x(self, *args, **kwargs):
        ''' Scroll canvas horizontally and redraw the image '''
        self.canvas.xview(*args, **kwargs)  # scroll horizontally
        self.show_image()  # redraw the image
        
    def move_from(self, event):
        ''' Remember previous coordinates for scrolling with the mouse '''
        self.canvas.scan_mark(event.x, event.y)

    def move_to(self, event):
        ''' Drag (move) canvas to the new position '''
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        self.show_image()  # redraw the image

    def wheel(self, event):
        ''' Zoom with mouse wheel '''
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        bbox = self.canvas.bbox(self.container)  # get image area
        if bbox[0] < x < bbox[2] and bbox[1] < y < bbox[3]: pass  # Ok! Inside the image
        else: return  # zoom only inside image area
        scale = 1.0
        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        if event.num == 5 or event.delta == -120:  # scroll down
            i = min(self.width, self.height)
            if int(i * self.imscale) < 30: return  # image is less than 30 pixels
            self.imscale /= self.delta
            scale        /= self.delta
        if event.num == 4 or event.delta == 120:  # scroll up
            i = min(self.canvas.winfo_width(), self.canvas.winfo_height())
            if i < self.imscale: return  # 1 pixel is bigger than the visible area
            self.imscale *= self.delta
            scale        *= self.delta
        #print(x,y)
        self.canvas.scale('all', x, y, scale, scale)  # rescale all canvas objects
        self.show_image()

    def show_image(self, event=None, h=1000, w=1000):
        ''' Show image on the Canvas '''
        bbox1 = self.canvas.bbox(self.container)  # get image area
        # Remove 1 pixel shift at the sides of the bbox1
        bbox1 = (bbox1[0] + 1, bbox1[1] + 1, bbox1[2] - 1, bbox1[3] - 1)
        bbox2 = (self.canvas.canvasx(0),  # get visible area of the canvas
                 self.canvas.canvasy(0),
                 self.canvas.canvasx(self.canvas.winfo_width()),
                 self.canvas.canvasy(self.canvas.winfo_height()))
        bbox = [min(bbox1[0], bbox2[0]), min(bbox1[1], bbox2[1]),  # get scroll region box
                max(bbox1[2], bbox2[2]), max(bbox1[3], bbox2[3])]
        if bbox[0] == bbox2[0] and bbox[2] == bbox2[2]:  # whole image in the visible area
            bbox[0] = bbox1[0]
            bbox[2] = bbox1[2]
        if bbox[1] == bbox2[1] and bbox[3] == bbox2[3]:  # whole image in the visible area
            bbox[1] = bbox1[1]
            bbox[3] = bbox1[3]
        self.canvas.configure(scrollregion=bbox)  # set scroll region
        x1 = max(bbox2[0] - bbox1[0], 0)  # get coordinates (x1,y1,x2,y2) of the image tile
        y1 = max(bbox2[1] - bbox1[1], 0)
        x2 = min(bbox2[2], bbox1[2]) - bbox1[0]
        y2 = min(bbox2[3], bbox1[3]) - bbox1[1]
        if int(x2 - x1) > 0 and int(y2 - y1) > 0:  # show image if it in the visible area
            x = min(int(x2 / self.imscale), self.width)   # sometimes it is larger on 1 pixel...
            y = min(int(y2 / self.imscale), self.height)  # ...and sometimes not
            image = self.image.crop((int(x1 / self.imscale), int(y1 / self.imscale), x, y))
            imagetk = PIL.ImageTk.PhotoImage(image.resize((int(x2 - x1), int(y2 - y1))))
            imageid = self.canvas.create_image(max(bbox2[0], bbox1[0]), max(bbox2[1], bbox1[1]),
                                               anchor='nw', image=imagetk)
            self.canvas.lower(imageid)  # set image into background
            self.canvas.imagetk = imagetk  # keep an extra reference to prevent garbage-collection

    def get_xy_position(self, event, parent):
        """Get the x and y position of the mouse event.

        Args:
            event: The mouse event.
            parent: The parent widget that contains mouse position properties.
        """
        parent.mouse_x = event.x
        parent.mouse_y = event.y

    
    def paint_mode(self, x, y, radius, parent):
        """
        Paint a circular region on image_f and update the mask image_m.
        """
        # Active label color as RGB tuple
        paint_c1 = tuple(parent.lab_color_rgb[int(parent.lab_acti) - 1])
    
        # Draw on image_f (color image)
        draw_img = PIL.ImageDraw.Draw(parent.image_f)
        draw_img.ellipse(
            [x - radius, y - radius, x + radius, y + radius],
            fill=paint_c1
        )
    
        # Draw on image_m (grayscale mask)
        draw_mask = PIL.ImageDraw.Draw(parent.image_m)
        draw_mask.ellipse(
            [x - radius, y - radius, x + radius, y + radius],
            fill=int(parent.lab_acti)
        )

    def erase_mode(self, x, y, radius, parent):
        """
        Erase a circular region by restoring original pixels in image_f
        and setting erased area to 0 in image_m.
        """
        # Create a circular mask for erased region
        erase_mask = PIL.Image.new("L", parent.image_f.size, 0)
        draw_erase = PIL.ImageDraw.Draw(erase_mask)
        draw_erase.ellipse(
            [x - radius, y - radius, x + radius, y + radius],
            fill=255
        )
    
        # Restore original image in erased region
        parent.image_f.paste(parent.image_c, mask=erase_mask)
    
        # Set erased region to label 0 in image_m
        draw_mask = PIL.ImageDraw.Draw(parent.image_m)
        draw_mask.ellipse(
            [x - radius, y - radius, x + radius, y + radius],
            fill=0
        )
    
    
    def draw_smth(self, event, parent):
        """
        Draws on the image based on the user's interaction (paint or erase mode).
    
        Args:
            event (tk.Event): The event triggered by the user's interaction (e.g., mouse click).
            parent: The parent object containing image_f, image_m, image_c, lab_color_rgb, etc.
        """
        # Get mouse position relative to image
        offset = self.canvas.bbox(self.container)
        x1, y1 = int(self.canvas.canvasx(event.x)), int(self.canvas.canvasy(event.y))
        x2, y2 = offset[0], offset[1]
        x = int((x1 - x2) / self.imscale)
        y = int((y1 - y2) / self.imscale)
    
        # Brush size (radius)
        paint_s = int(parent.mouse_s / 2.0)
    
        if parent.paint_mode == "activated":
            self.paint_mode(x, y, paint_s, parent)
        elif parent.erase_mode == "activated":
            self.erase_mode(x, y, paint_s, parent)
            
        ## Create new image to be shown
        self.image = parent.image_f.copy()
        
        self.show_image()

    def reset_view(self):
        ## Update canvas
        self.canvas.update()

        ## Configure the scrolls
        #vbar.configure(command=self.scroll_y)  # bind scrollbars to the canvas
        #hbar.configure(command=self.scroll_x)
        self.canvas.delete("all")
        self.container = None
        self.image_id = None
        self.imscale, self.delta = 1.0, 1.3
        #self.canvas.xview_moveto(0)
        #self.canvas.yview_moveto(0)

    def refresh_from_parent(self, parent):
        """
        Refresh the canvas image from the parent object's current display image.
        Used after the parent updates parent.image_f or parent.image_m.
        """
        # Update internal copy and redraw
        #self.image = parent.image_f.copy()
        #self.width, self.height = self.image.size
        #self.show_image()
        
        ##
        self.reset_view()
        
        self.image = parent.image_f.copy()
           
        ## Set width and height of image
        self.width, self.height = self.image.size[0], self.image.size[1]
        
        ## Compute the offset
        offset = self.computeoffset(self.canvas.winfo_height(),
                                    self.canvas.winfo_width(),
                                    self.height,self.width)
        
        ## Set container.
        self.container = self.canvas.create_rectangle(offset[0], offset[1], self.width+offset[0], self.height+offset[1])
        
        #self.container = self.canvas.create_rectangle(offx, offy, offx + self.width, offy + self.height,outline="", width=0)
        
        
        self.canvas.configure(scrollregion=(offset[0], offset[1], self.width + offset[0], self.height+offset[1]))
        
        ## Show image has to be initialized here otherwize
        self.show_image(self.canvas.winfo_height(),self.canvas.winfo_height())
        
        
        
        #def reset_view(self):
    
        


class ImageWindowPmButtons(ttk.Frame):
    """A frame widget that manages buttons for navigating through images.

    Attributes:
        parent (ttk.Tk): The parent window.
    """

    def __init__(self, parent):
        """Initialize the frame and place it within the parent widget.

        Args:
            parent: The parent widget in which this frame is placed.
        """
        super().__init__(parent)
        self.place(relx=0.320, rely=0.55 + 0.06 + 0.3, relwidth=0.67,
                   relheight=0.06)
        self.create_widget(parent)

    def create_widget(self, parent):
        """Create and configure the navigation buttons.

        Args:
            parent: The parent widget in which the buttons are placed.
        """
        # Create buttons
        ba = ttk.Button(self, text='<<',
                        command=lambda: self.leftright_button(parent, False))
        bm = ttk.Button(self, text='>>',
                        command=lambda: self.leftright_button(parent, True))
        # Set packmanager options
        ba.pack(side='left', anchor='e', expand=True, fill='both')
        bm.pack(side='right', anchor='w', expand=True, fill='both')

    @staticmethod
    def leftright_button(parent, toggle):
        """Update the image index based on the toggle direction.
    
        Args:
            parent: The parent widget containing the image list and index.
            toggle: A boolean indicating whether to move forward (True) or backward (False).
        """
        # Create directory string to the mask folder
        masks_folder = Path(parent.filedirectory) / "output" / "masks"
        masks_folder.mkdir(parents=True, exist_ok=True)  # Ensure folder exists
    
        # Create mask file name
        mask_filename = Path(parent.current_image_path).stem + '_mask.npy'
        mask_path = masks_folder / mask_filename
    
        # Check if object parent contains image_m and investigate if image_m has any label different from zero
        if hasattr(parent, 'image_m') and np.any(np.array(parent.image_m)):
            # Save mask
            np.save(mask_path, np.array(parent.image_m))
            #print(f"Auto-saved mask: {mask_path.name}")
    
            # Add to training_image_paths if not already there
            if str(parent.current_image_path) not in parent.training_image_paths:
                parent.training_image_paths.append(str(parent.current_image_path))
    
            # Add to training_mask_paths if not already there
            if str(mask_path) not in parent.training_mask_paths:
                parent.training_mask_paths.append(str(mask_path))
                
            # Refresh UI if Training Set Manager exists
            if hasattr(parent, 'training_set_manager'):
                parent.training_set_manager.refresh()
                
        else:
            # Delete mask file from disk if it exists
            if mask_path.exists():
                mask_path.unlink()
                #print(f"Deleted empty mask: {mask_path.name}")
    
            # Remove from training_image_paths and training_mask_paths
            if str(parent.current_image_path) in parent.training_image_paths:
                idx = parent.training_image_paths.index(str(parent.current_image_path))
                parent.training_image_paths.pop(idx)
                parent.training_mask_paths.pop(idx)
    
        # Check if any images are loaded
        if len(parent.img_filenames) == 0:
            ImageWindow(parent)
            return
        
        # Update image index
        if toggle is True:
            parent.img_numb  = parent.img_numb + 1
            if parent.img_numb > len(parent.img_filenames)-1:
                parent.img_numb = len(parent.img_filenames) - 1
        if toggle is False:
            parent.img_numb  = parent.img_numb - 1
            if parent.img_numb < 0:
                parent.img_numb = 0
        
        # Get the new image
        img_filename = parent.img_filenames[parent.img_numb]
        
        #parent.image_c = PIL.Image.open(img_filename)
        
        parent.image_c = ensure_rgba(img_filename)
        parent.image_f = parent.image_c.copy()
    
        # Set current image path
        parent.current_image_path = img_filename
    
        # Create mask file name for new image
        mask_filename = Path(parent.current_image_path).stem + '_mask.npy'
        mask_path = masks_folder / mask_filename
    
        # Check if mask exists
        if mask_path.exists():
            print(f"Loading existing mask: {mask_path.name}")
            mask_array = np.load(mask_path)
            parent.image_m = PIL.Image.fromarray(mask_array.astype(np.uint8), mode="L")
    
            # Impose mask on image_f
            img_array = np.array(parent.image_f)
            mask_data = np.array(parent.image_m)
    
            # Replace RGB values at mask indices with corresponding colors
            for label_idx, rgb in enumerate(parent.lab_color_rgb, start=1):
                img_array[mask_data == label_idx, :3] = rgb  # Replace only RGB channels
    
            # Convert back to PIL after NumPy modification
            parent.image_f = PIL.Image.fromarray(img_array, mode="RGBA")
        else:
            #print(f"No mask found for {parent.current_image_path}, creating blank mask.")
            parent.image_m = PIL.Image.new("L", parent.image_c.size, 0)
    
        # Call image window to display the image
        #ImageWindow(parent)
        
        # Refresh image window
        parent.image_window.refresh_from_parent(parent)
    
        # Refresh UI if Training Set Manager exists
        #if hasattr(parent, 'training_set_manager'):
        #    parent.training_set_manager.refresh()
        
        # Refresh UI if image toogle text exist
        if hasattr(parent, 'image_toogle_text'):
           parent.image_toogle_text.update_widget(parent)
#
# https://stackoverflow.com/questions/69050464/zoom-into-image-with-opencv
# https://stackoverflow.com/questions/17355902/tkinter-binding-mousewheel-to-scrollbar
# https://gist.github.com/i-namekawa/74a817683b0e68cee521
# https://pythontutorialsolveissue.blogspot.com/2019/11/python-zoom-in-zoom-out-image.html
# https://stackoverflow.com/questions/41656176/tkinter-canvas-zoom-move-pan/48137257#48137257