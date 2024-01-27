import tkinter as tk
from src.frames import AddEditDVDFrame

class DVDAddView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='#555')
        self.__controller = controller
        self.__create_view()

    def __create_view(self):
        self.__ae_dvd_frame = AddEditDVDFrame(self, self.__controller, 'add', -1)
        self.__ae_dvd_frame.pack()

