import tkinter as tk
from tkinter import ttk
from src.frames import AddEditDVDFrame

class DVDAddView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.ae_dvd_frame = AddEditDVDFrame(self, self, 'add', -1)
        self.ae_dvd_frame.pack()

