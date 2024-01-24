import tkinter as tk
from tkinter import ttk

class PhysicalRemoveFrame(ttk.Frame):
    def __init__(self, parent, controller, code):
        super().__init__(parent)
        self.controller = controller
        self.code = code

        ttk.Label(self, text=code, width=10).pack(anchor='w', side='left')
        ttk.Button(self, text='Usuń', command=self.on_delete_pressed).pack(side='left')

    def on_delete_pressed(self):
        self.controller.del_code(self.code)
        self.destroy()

    def get_code(self):
        return self.code
