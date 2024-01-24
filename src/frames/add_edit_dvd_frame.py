import tkinter as tk
from tkinter import ttk
from datetime import datetime
from src.database.models import DVDModel
from src.database.models import PhysicalDVDModel
from src.database.models import CategoryModel
from src.database.models import DVDCategoryRelationModel
from src.frames.categories_frame import CategoriesFrame
from src.frames.physical_copies_frame import PhysicalCopiesFrame

class AddEditDVDFrame(ttk.Frame):
    def __init__(self, parent, controller, f_type, dvd_id):
        super().__init__(parent)
        self.dvd_id = dvd_id
        self.f_type = f_type
        self.title = "Edycja płyty DVD" if f_type == 'edit' else "Dodawanie płyty DVD"

        self.name_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.categories_var = tk.StringVar()
        self.physical_var = tk.StringVar()

        self.create_frame()

    def create_frame(self):
        # Tytuł widoku
        ttk.Label(self, text=self.title, font=('Arial', 22)).pack(pady=(8,20))

        # uzupełnianie pól nazwy i daty
        dvd_rows = DVDModel.select({'id': self.dvd_id})
        if len(dvd_rows) > 0:
            model = dvd_rows[0]
            self.name_var.set(model.name)
            self.date_var.set(str(datetime.fromtimestamp(model.date).strftime("%d/%m/%Y")))
        # Przycisk do usuwania
        if self.f_type == 'edit':
            ttk.Button(self, text="Usuń płytę DVD", command=self.delete_dvd).pack(anchor='e', pady=(0,20), padx=(0,40))
        # Pole do wpisania nazwy
        ttk.Label(self, text='Nazwa', font=('Arial', 16)).pack(anchor='w')
        ttk.Entry(self, textvariable=self.name_var, width=30).pack(anchor='w', pady=(8,20))
        # Pole do wpisania roku wydania
        ttk.Label(self, text='Rok wydania', font=('Arial', 16)).pack(anchor='w')
        ttk.Entry(self, textvariable=self.date_var, width=30).pack(anchor='w', pady=(8,20))
        # Kontener (Frame) na kategorie i fizyczne kopie
        ctgy_copy_container = ttk.Frame(self)
        ctgy_copy_container.pack(anchor='w')
        # Kategorie
        self.categories_frame = CategoriesFrame(ctgy_copy_container, self, self.dvd_id)
        self.categories_frame.pack(side='left', anchor='nw')
        # Fizyczne kopie
        self.physical_copies_container = PhysicalCopiesFrame(ctgy_copy_container, self, self.dvd_id)
        self.physical_copies_container.pack(anchor='nw', side='left', padx='50')
        # Przycisk do stworzenia zapisu o płycie DVD
        if self.f_type == 'edit':
            ttk.Button(self, text='Aktualizuj', command=self.update).pack()
        else:
            ttk.Button(self, text="Stwórz", command=self.create).pack()

    def create(self):
        name = self.name_var.get()
        date = datetime.strptime(self.date_var.get(), "%d/%m/%Y")
        DVDModel.insert({'name': name, 'date':date})
        self.dvd_id = DVDModel.select({'name': name, 'date':date})[0].get_id()
        self.update_categories()
        self.update_physical_dvds()

    def update(self):
        # Aktualizacja nazwy i daty
        name = self.name_var.get()
        date = datetime.strptime(self.date_var.get(), "%d/%m/%Y")
        DVDModel.select({'id': self.dvd_id})[0].update(
            {'name': name, 'date': date}
        )
        self.update_categories()
        self.update_physical_dvds()

    def update_categories(self):
        relations = DVDCategoryRelationModel.select({'dvd_id': self.dvd_id})
        current_categories_ids = [ relation.get_category_id() for relation in relations ]
        this_categories_names = []
        [ this_categories_names.append(name) for name, str_var in self.categories_frame.category_vars.items() \
            if str_var.get() == 'true' ]
        this_categories_ids = [ CategoryModel.select({'name': name})[0].get_id() for name in this_categories_names ]

        add_categories_ids = []
        del_categories_ids = []
        [ add_categories_ids.append(id) for id in this_categories_ids if id not in current_categories_ids ]
        [ del_categories_ids.append(id) for id in current_categories_ids if id not in this_categories_ids ]

        for category_id in add_categories_ids:
            DVDCategoryRelationModel.insert(
                {'dvd_id': self.dvd_id, 'category_id': category_id}
            )
        
        DVDCategoryRelationModel.delete_where(
            {'dvd_id': self.dvd_id, 'category_id': del_categories_ids}
        )

    def update_physical_dvds(self):
        physical_dvds = PhysicalDVDModel.select({'dvd_id': self.dvd_id})
        current_codes = [ p_dvd.get_physical_code() for p_dvd in physical_dvds ]
        add_codes = []
        del_codes = []
        print(self.physical_copies_container.physical_codes)

        # Jeśli kod z physical_codes nie jest w current_codes to znaczy że trzeba go dodać
        [ add_codes.append(code) for code in self.physical_copies_container.physical_codes \
            if code not in current_codes ]

        # Jeśli kod z current_codes nie jest w physical_codes to znaczy że trzeba go usunąć
        [ del_codes.append(code) for code in current_codes \
            if code not in self.physical_copies_container.physical_codes ]
        # Dodaj wszystkie kody z add_codes
        for code in add_codes:
            PhysicalDVDModel.insert({
                'physical_code': code,
                'dvd_id': self.dvd_id,
                'rental_state_id': 1
            })
        # Usuń wszystkie wpisy z kodami z del_codes
        PhysicalDVDModel.delete_where({
            'dvd_id': self.dvd_id,
            'physical_code': del_codes
        })

    def delete_dvd(self):
        DVDModel.delete_where({'id': self.dvd_id})
