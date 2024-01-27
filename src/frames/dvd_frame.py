import tkinter as tk
from datetime import datetime
from src.database.models import DVDCategoryRelationModel
from src.database.models import CategoryModel
from src.database.models import PhysicalDVDModel


class DVDFrame(tk.Frame):
    def __init__(self, parent, controller, dvd_model):
        super().__init__(parent, width=650, height=160, background='#333333')
        self.pack_propagate(0)
        self.__bg_color = '#333333'
        self.__dvd_model = dvd_model
        self.__controller = controller
        self.__create_frame()

    def __create_frame(self):
        category_relations = DVDCategoryRelationModel.select({'dvd_id': self.__dvd_model.get_id()})
        print(category_relations)
        
        physical_dvds = PhysicalDVDModel.select({'dvd_id': self.__dvd_model.get_id()})

        top_frame = tk.Frame(self, background=self.__bg_color)
        top_frame.pack(fill='x', padx=10, pady=10)

        tk.Label(
            top_frame, text=self.__dvd_model.get_name() + f' ({len(physical_dvds)})', font=('Arial', 20),
            background=self.__bg_color, foreground='white'
        ).pack(anchor='w', side='left')
        
        tk.Label(top_frame, text=str(
            datetime.fromtimestamp(self.__dvd_model.get_date()).strftime("%d/%m/%Y")), font=('Arial', 16),
            background=self.__bg_color, foreground='white'
        ).pack(side='right')

        cat_continer = tk.Frame(self, background=self.__bg_color)
        cat_continer.pack(anchor='w')

        for relation in category_relations:
            cat_color = '#5555aa'
            category = CategoryModel.select({'id': relation.get_category_id()})[0]
            cat_frame = tk.Frame(cat_continer, background=cat_color)
            cat_frame.pack(padx=10, side='left')
            lab = tk.Label(cat_frame, text=category.get_name(), font=('Arial', 16), 
                           background=cat_color, foreground='white'
                           )
            lab.pack(padx=5, pady=2)

        buttons_frame = tk.Frame(self, background=self.__bg_color)
        buttons_frame.pack(fill='x', side='bottom')

        tk.Button(buttons_frame, text="Wyporzycz", command=self.__dvd_borrow_view,
                  background='white', fg='black',
                  font=("Arial", 14)
                   ).pack(side='left' , padx=30, pady=10)
        tk.Button(buttons_frame, text="Edytuj", command=self.__dvd_edit_view,
                  background='white', fg='black',
                  font=("Arial", 14)
                   ).pack(side='right', padx=30, pady=10)

    def __dvd_borrow_view(self):
        self.__controller.set_selected_dvd_id(self.__dvd_model.get_id())
        self.__controller.dvd_borrow_view()

    def __dvd_edit_view(self):
        self.__controller.set_selected_dvd_id(self.__dvd_model.get_id())
        self.__controller.dvd_edit_view()
