from tkinter import ttk
import tkinter as tk
from datetime import datetime
from src.database.models import DVDCategoryRelationModel
from src.database.models import CategoryModel
from src.database.models import PhysicalDVDModel


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
        category_relations = DVDCategoryRelationModel.select({'dvd_id': self.dvd_model.get_id()})
        print(category_relations)
        for relation in category_relations:
            category = CategoryModel.select({'id': relation.get_category_id()})[0]
            lab = ttk.Label(cat_frame, text=category.get_name())
            lab.pack(padx=10, side='left')
        
        physical_dvds = PhysicalDVDModel.select({'dvd_id': self.dvd_model.get_id()})
        ttk.Label(self, text=f"liczba kopii: {len(physical_dvds)}").pack(anchor='w')
        ttk.Button(self, text="Wyporzycz", command=self.dvd_borrow_view).pack(side='left')
        ttk.Button(self, text="Edytuj", command=self.dvd_edit_view).pack(side='left')

    def dvd_borrow_view(self):
        self.controller.selected_dvd = self.dvd_model.get_id()
        self.controller.dvd_borrow_view()

    def dvd_edit_view(self):
        self.controller.selected_dvd = self.dvd_model.get_id()
        self.controller.dvd_edit_view()
