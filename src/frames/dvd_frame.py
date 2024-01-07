from tkinter import ttk
import tkinter as tk
from datetime import datetime

class DVDFrame(ttk.Frame):
    def __init__(self, parent, controller, dvd_model):
        super().__init__(parent)
        self.dvd_model = dvd_model
        self.controller = controller

        ttk.Label(self, text=self.dvd_model.name).pack(anchor='w')
        ttk.Label(self, text="Opis filmu").pack(anchor='w')
        ttk.Label(self, text=str(
            datetime.fromtimestamp(self.dvd_model.date).strftime("%d/%m/%Y")
        )).pack(anchor='w')

        cat_frame = ttk.Frame(self)
        cat_frame.pack(anchor='w')
        for i in range(4): # tworzenie poglądowych kategorii
            lab = ttk.Label(cat_frame, text="Category")
            lab.pack(padx=10, side='left')
        ttk.Label(self, text="liczba kopii: 2").pack(anchor='w')
        ttk.Button(self, text="Wyporzycz", command=self.dvd_borrow_view).pack(side='left')
        ttk.Button(self, text="Edytuj", command=self.dvd_edit_view).pack(side='left')

    def dvd_borrow_view(self):
        self.controller.selected_dvd = self.dvd_model.get_id()
        self.controller.dvd_borrow_view()

    def dvd_edit_view(self):
        self.controller.selected_dvd = self.dvd_model.get_id()
        self.controller.dvd_edit_view()
