import tkinter as tk
from tkinter import ttk
from src.frames.category_checkbox_frame import CategoryCheckboxFrame
from src.database.models import CategoryModel
from src.database.models import DVDCategoryRelationModel

class CategoriesFrame(ttk.Frame):
    def __init__(self, parent, controller, dvd_id):
        super().__init__(parent)
        self.dvd_id = dvd_id
        self.category_vars = {}
        self.create_frame()
    
    def create_frame(self):
        category_container = ttk.Frame(self)
        category_container.pack(anchor='nw', side='left', padx='50')
        ttk.Label(category_container, text='Kategorie', font=('Arial', 16)).pack(anchor='w')
        categories = CategoryModel.select()
        relations = DVDCategoryRelationModel.select({'dvd_id': self.dvd_id})
        categories_ids = [relation.get_category_id() for relation in relations]
        for cat in categories:
            s_var = tk.StringVar()
            s_var.set('true' if cat.get_id() in categories_ids else 'false')
            self.category_vars[f'{cat.get_name()}'] = s_var
            cat_frame = CategoryCheckboxFrame(category_container, self, cat.name, s_var)
            cat_frame.pack(anchor='w')


