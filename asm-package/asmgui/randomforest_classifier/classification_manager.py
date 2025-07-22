## Load in packages
import tkinter as tk

class FeatureSelector(tk.Frame):
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
        l1 = tk.Label(self, width=15, text='Select Features',
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