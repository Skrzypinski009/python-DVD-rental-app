import tkinter as tk
from tkinter import ttk

class CategoryCheckboxFrame(ttk.Frame):
    def __init__(self, parent, controller, name):
        super().__init__(parent)
        self.str_val = tk.StringVar()
        self.value = 'false'
        self.name = name
        ttk.Checkbutton(
            self.container, 
            text=self.name, 
            variable = str_val,
            onvalue='true',
            offvalue='false',
            font=controller.med_font
        ).pack(anchor='w')

    def on_click(self):
        self.value = str_val.get()

