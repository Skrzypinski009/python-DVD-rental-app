import tkinter as tk
from tkinter import ttk

class PhysicalRemoveFrame(tk.Frame):
    def __init__(self, parent, controller, code):
        super().__init__(parent, bg='#555')
        self.__controller = controller
        self.__code = code

        tk.Label(self, text=code, width=10, bg='#555', fg='white').pack(anchor='w', side='left')
        tk.Button(self, text='Usuń', command=self.__on_delete_pressed).pack(side='left')

    def __on_delete_pressed(self):
        self.__controller.del_code(self.__code)
        self.destroy()

    def get_code(self):
        return self.__code
