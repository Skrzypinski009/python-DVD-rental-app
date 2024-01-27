import tkinter as tk
from tkinter import ttk

class CategoryCheckboxFrame(tk.Frame):
    def __init__(self, parent, controller, name, s_var):
        super().__init__(parent, bg='#555')
        self.__str_var = s_var
        self.__name = name
        tk.Checkbutton(
            self, 
            variable = self.__str_var,
            onvalue='true',
            offvalue='false',
            bg='#555',
            highlightthickness=0, 
            relief='flat'
        ).pack(anchor='w', fill='none', side='left')
        tk.Label(
            self, text=self.__name, font=('Arial', 14),
            bg='#555', fg='white'
        ).pack(anchor='w', fill='none', side='left')

