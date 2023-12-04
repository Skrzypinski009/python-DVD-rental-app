from tkinter import ttk
import tkinter as tk

class DVDSearchView(ttk.Frame):
    def __init__(self, parent, controler):
        super().__init__(parent, width=parent.winfo_reqwidth())
        self.configure(style='View.TFrame')
        for i in range(0,40):
            label = ttk.Label(self, text="DVDSearchView")
            label.configure(style='View.TLabel')
            label.pack()
