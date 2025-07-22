"""The module manages status of on the main frame window"""
import tkinter as tk
from tkinter import ttk


class StatusManager(tk.Frame):
    """
    Frame widget for managing the status of the ASM application.

    Attributes:
        parent (tk.Tk): The parent window.
    """
    def __init__(self, parent):
        """
        Initialize StatusManager frame.

        Args:
            parent: The parent widget.
        """
        super().__init__(parent)
        self.place(x=0.5, rely=0.225, relwidth=0.25, relheight=0.3)
        self.create_widget(parent)

    def create_widget(self, parent):
        """
        Create labels, text widget, and button for status management.

        Args:
            parent: The parent widget.
        """
        l1 = tk.Label(self, width=15, text='Status Manager',
                      font=('Times', 24), anchor="w", background='white')
        tw = tk.Text(self, width=15)
        scrollbar = tk.Scrollbar(tw, command=tw.yview)
        tw.configure(yscrollcommand=scrollbar.set)
        b = tk.Button(self, width=20, text='update',
                      command=lambda: self.clicked_update(tw, scrollbar, parent))

        l1.pack(expand=True, fill='both')
        b.pack(expand=True, fill='both')
        tw.pack(expand=True, fill='both')
        scrollbar.pack(side=tk.RIGHT, fill='y')

    @staticmethod
    def clicked_update(tw, scrollbar, parent):
        """
        Update the status text widget.

        Args:
            tw: The text widget.
            scrollbar: The scrollbar widget.
            parent: The parent widget.
        """
        for i in range(0, len(parent.img_name)):
            tw.insert(tk.END, parent.img_name[i] + "\n")
        tw.configure(yscrollcommand=scrollbar.set)
        tw.configure(state=tk.DISABLED)
        print('Images updated')
    
    
class LabelManagerText(ttk.Frame):
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
        self.place(x=5.0, rely=0.095, relwidth=0.15, relheight=0.04)
        self.create_widget(parent)

    def create_widget(self, parent):
        """
        Create and configure the label widget.

        Args:
            parent: The parent widget.
        """
        #HEADER TITLE
        l = ttk.Label(self, text="🔖 Label manager", 
              font=('Times', 24), anchor="w", justify="left")
        l.grid(row=0, column=0, sticky='w', padx=5, pady=(5, 10))


class LabelManagerPmButtons(ttk.Frame):
    """
    A frame widget for managing label buttons.

    Attributes:
        parent (ttk.Tk): The parent window.
    """

    def __init__(self, parent):
        """
        Initialize LabelManagerPmButtons frame.

        Args:
            parent: The parent widget.
        """
        super().__init__(parent)
        self.place(x=5, rely=0.095 + 0.04+2.0*0.08, relwidth=0.15, relheight=0.03)
        # Create widget
        self.create_widget(parent)

    def create_widget(self, parent):
        """
        Create buttons for adding and removing labels.

        Args:
            parent: The parent widget.
        """
        
        ba = tk.Button(self, text='+',
                        font=("Segoe UI", 10),
                        relief="solid", bd=1,  # Solid border
                        highlightthickness=1,
                        padx=20, pady=0,       # Reduce vertical padding
                        height=1,      
                        command=lambda: self.add_button(parent))
        bm = tk.Button(self, text='-',
                        font=("Segoe UI", 10),
                        relief="solid", bd=1,  # Solid border
                        highlightthickness=1,
                        padx=20, pady=0,       # Reduce vertical padding
                        height=1,      
                        command=lambda: self.min_button(parent))
        ba.pack(side='left', anchor='e', expand=True, fill='both')
        bm.pack(side='right', anchor='w', expand=True, fill='both')

    @staticmethod
    def add_button(parent):
        """
        Add a label to the parent widget's label list and update the display.

        Args:
            parent: The parent widget.
        """
        if len(parent.lab_name) == 0:
            parent.lab_name.append(1)
            LabelManagerLabels(parent)
        else:
            parent.lab_name.append(parent.lab_name[-1] + 1)
            LabelManagerLabels(parent)

    @staticmethod
    def min_button(parent):
        """
        Remove the last label from the parent widget's label list and update the display.

        Args:
            parent: The parent widget.
        Prints a message if there are no labels to remove.
        """
        if len(parent.lab_name) == 0:
            print('no labels to remove, add a label to remove one')
        else:
            del parent.lab_name[-1]
            LabelManagerLabels(parent)
            

class LabelManagerLabels(ttk.Frame):
    """
    A frame widget that manages the display and status of labels.

    Attributes:
        parent (ttk.Tk): The parent window.
    """

    def __init__(self, parent):
        """
        Initialize LabelManagerLabels frame, place it within the parent widget, 
        and create labels if any exist.

        Args:
            parent: The parent widget.
        """
        super().__init__(parent,borderwidth=2, relief="solid")
        self.place(x=5, rely=0.095 + 0.04, relwidth=0.15, relheight=2.0*0.08)
        #print('Label added')
        if len(parent.lab_name) > 0:
            self.create_widget(parent)

    def create_widget(self, parent):
        """
        Create and configure the label buttons based on the parent's label list.

        Args:
            parent: The parent widget whose label list determines the label buttons.
        """
        btn_list = []
        for i in range(1, len(parent.lab_name) + 1):
            if i == parent.lab_acti:
                btn_n = "Label " + str(i) + " , status - activated"
            else:
                btn_n = "Label " + str(i) + " , status - deactivated"
            
            ## Update button
            btn_t = tk.Button(self, width=20, text=btn_n,
                              font=("Segoe UI", 10),
                              relief="solid", bd=0,  # Solid border
                              #highlightthickness=1,
                              command=lambda i=i: self.update_widget(i, parent,
                                                                      btn_list))
            btn_list.append(btn_t)
            btn_t.pack(expand=True, fill='both')
            
    @staticmethod
    def update_widget(ith, parent, btn_list):
        """
        Update the status of the label buttons and print the activated label number.

        Args:
            ith: The index of the label to be activated.
            parent: The parent widget whose label list is to be updated.
            btn_list: The list of button widgets representing labels.
        """
        parent.lab_acti = str(ith)
        print('Updating activated label = ' + str(ith))
        for j in range(1, len(btn_list) + 1):
            if j == ith:
                #print(j, ith)
                btn_list[j - 1]["text"] = "Label " + str(
                    j) + " , status - activated"
            else:
                btn_list[j - 1]["text"] = "Label " + str(
                    j) + " , status - deactivated"
                               
    def refresh(self, parent):
        """
        Refresh the label buttons to reflect the current state of parent's label list.
        """
        # Destroy all existing widgets in this frame
        for widget in self.winfo_children():
            widget.destroy()

        # Recreate the buttons based on updated parent.lab_name
        self.create_widget(parent)
