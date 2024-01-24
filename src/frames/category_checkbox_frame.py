import tkinter as tk
from tkinter import ttk

class CategoryCheckboxFrame(ttk.Frame):
    def __init__(self, parent, controller, name, s_var):
        super().__init__(parent)
        self.str_var = s_var
        self.name = name
        ttk.Checkbutton(
            self, 
            variable = self.str_var,
            onvalue='true',
            offvalue='false',
        ).pack(anchor='w', fill='none', side='left')
        ttk.Label(self, text=self.name, font=('Arial', 14)).pack(anchor='w', fill='none', side='left')

