import tkinter as tk
from tkinter import ttk
from src.frames.category_checkbox_frame import CategoryCheckboxFrame
from src.database.models import CategoryModel
from src.database.models import DVDCategoryRelationModel

class CategoriesFrame(tk.Frame):
    def __init__(self, parent, controller, dvd_id):
        super().__init__(parent, bg='#555')
        self.__dvd_id = dvd_id
        self.__category_vars = {}
        self.__create_frame()

    def get_category_vars(self):
        return self.__category_vars
    
    def __create_frame(self):
        category_container = tk.Frame(self, bg='#555')
        category_container.pack(anchor='nw', side='left', padx='50')
        tk.Label(
            category_container, text='Kategorie', font=('Arial', 16),
            bg='#5555aa', fg='white'
        ).pack(anchor='w')
        categories = CategoryModel.select()
        relations = DVDCategoryRelationModel.select({'dvd_id': self.__dvd_id})
        categories_ids = [relation.get_category_id() for relation in relations]
        for cat in categories:
            s_var = tk.StringVar()
            s_var.set('true' if cat.get_id() in categories_ids else 'false')
            self.__category_vars[f'{cat.get_name()}'] = s_var
            cat_frame = CategoryCheckboxFrame(category_container, self, cat.get_name(), s_var)
            cat_frame.pack(anchor='w')

