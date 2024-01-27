import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from src.database.database_manager import DatabaseManager
from src.database.models import DVDModel
from src.database.models import PhysicalDVDModel
from src.database.models import CategoryModel
from src.database.models import DVDCategoryRelationModel
from src.frames.categories_frame import CategoriesFrame
from src.frames.physical_copies_frame import PhysicalCopiesFrame

class AddEditDVDFrame(tk.Frame):
    def __init__(self, parent, controller, f_type, dvd_id):
        super().__init__(parent, background='#555')
        self.__bg_color = '#555'
        self.__controller = controller
        self.__dvd_id = dvd_id
        self.__f_type = f_type
        self.__title = "Edycja płyty DVD" if f_type == 'edit' else "Dodawanie płyty DVD"

        self.__name_var = tk.StringVar()
        self.__date_var = tk.StringVar()
        self.__categories_var = tk.StringVar()
        self.__physical_var = tk.StringVar()

        self.__create_frame()

    def __create_frame(self):
        # Tytuł widoku
        tk.Label(
            self, text=self.__title, font=('Arial', 22),
            bg=self.__bg_color, fg='white'
        ).pack(pady=(8,20))
        # uzupełnianie pól nazwy i daty
        dvd_rows = DVDModel.select({'id': self.__dvd_id})
        if len(dvd_rows) > 0:
            model = dvd_rows[0]
            self.__name_var.set(model.get_name())
            self.__date_var.set(str(datetime.fromtimestamp(model.get_date()).strftime("%d/%m/%Y")))
        # Przycisk do usuwania
        if self.__f_type == 'edit':
            tk.Button(
                self, text="Usuń płytę DVD", command=self.__delete_dvd,
                bg='#333', fg='white', activebackground='#444', activeforeground='white',
                highlightthickness=0, relief='flat'
            ).pack(anchor='e', pady=(0,20), padx=(0,40))
        # Pole do wpisania nazwy
        tk.Label(
            self, text='Nazwa', font=('Arial', 16), bg=self.__bg_color, fg='white'
        ).pack(anchor='w')
        tk.Entry(
            self, textvariable=self.__name_var, width=30
        ).pack(anchor='w', pady=(8,20))
        # Pole do wpisania roku wydania
        tk.Label(
            self, text='Data wydania (DD/MM/YYYY)', font=('Arial', 16),
            bg=self.__bg_color, fg='white'
        ).pack(anchor='w')
        ttk.Entry(self, textvariable=self.__date_var, width=30).pack(anchor='w', pady=(8,20))
        # Kontener (Frame) na kategorie i fizyczne kopie
        ctgy_copy_container = tk.Frame(self, bg=self.__bg_color)
        ctgy_copy_container.pack(anchor='w')
        # Kategorie
        self.__categories_frame = CategoriesFrame(ctgy_copy_container, self, self.__dvd_id)
        self.__categories_frame.pack(side='left', anchor='nw')
        # Fizyczne kopie
        self.__physical_copies_container = PhysicalCopiesFrame(ctgy_copy_container, self, self.__dvd_id)
        self.__physical_copies_container.pack(anchor='nw', side='left', padx='50')
        # Przycisk do stworzenia zapisu o płycie DVD
        if self.__f_type == 'edit':
            tk.Button(
                self, text='Aktualizuj', command=self.__update,
                bg='#333', fg='white', activebackground='#444', activeforeground='white',
                highlightthickness=0, relief='flat', font=('Arial', 14)
            ).pack()
        else:
            tk.Button(
                self, text="Stwórz", command=self.__create,
                bg='#333', fg='white', activebackground='#444', activeforeground='white',
                highlightthickness=0, relief='flat', font=('Arial', 14)
            ).pack()
        self.__warning_label = tk.Label(self, text='', bg=self.__bg_color, fg='red')
        self.__warning_label.pack()

    def __create(self):
        name = self.__name_var.get()
        if name == '':
            self.__warning_label.configure(text='Wprowadź nazwę!')
            return
        try:
            date = datetime.strptime(self.__date_var.get(), "%d/%m/%Y")
        except:
            self.__warning_label.configure(text='Wprowadź poprawną datę!')
            return
        DVDModel.insert({'name': name, 'date':date})
        self.__dvd_id = DVDModel.select({'name': name, 'date':date})[0].get_id()
        self.__update_categories()
        self.__update_physical_dvds()
        messagebox.showinfo(title='DVD add', message='Płyta dodana pomyślnie!')
        self.__quit_view()


    def __update(self):
        name = self.__name_var.get()
        if name == '':
            self.__warning_label.configure(text='Wprowadź nazwę!')
            return
        try:
            date = datetime.strptime(self.__date_var.get(), "%d/%m/%Y")
        except:
            self.__warning_label.configure(text='Wprowadź poprawną datę!')
            return
        DVDModel.select({'id': self.__dvd_id})[0].update(
            {'name': name, 'date': date}
        )
        self.__update_categories()
        self.__update_physical_dvds()
        messagebox.showinfo(title='DVD edit', message='Płyta zaktualizowana pomyślnie!')
        self.__quit_view()

    def __update_categories(self):
        relations = DVDCategoryRelationModel.select({'dvd_id': self.__dvd_id})
        current_categories_ids = [ relation.get_category_id() for relation in relations ]
        this_categories_names = []
        [ this_categories_names.append(name) for name, str_var in self.__categories_frame.get_category_vars().items() \
            if str_var.get() == 'true' ]
        this_categories_ids = [ CategoryModel.select({'name': name})[0].get_id() for name in this_categories_names ]

        add_categories_ids = []
        del_categories_ids = []
        [ add_categories_ids.append(id) for id in this_categories_ids if id not in current_categories_ids ]
        [ del_categories_ids.append(id) for id in current_categories_ids if id not in this_categories_ids ]

        for category_id in add_categories_ids:
            DVDCategoryRelationModel.insert(
                {'dvd_id': self.__dvd_id, 'category_id': category_id}
            )
        
        DVDCategoryRelationModel.delete_where(
            {'dvd_id': self.__dvd_id, 'category_id': del_categories_ids}
        )

    def __update_physical_dvds(self):
        physical_dvds = PhysicalDVDModel.select({'dvd_id': self.__dvd_id})
        current_codes = [ p_dvd.get_physical_code() for p_dvd in physical_dvds ]
        add_codes = []
        del_codes = []

        # Jeśli kod z physical_codes nie jest w current_codes to znaczy że trzeba go dodać
        [ add_codes.append(code) for code in self.__physical_copies_container.get_physical_codes() \
            if code not in current_codes ]

        # Jeśli kod z current_codes nie jest w physical_codes to znaczy że trzeba go usunąć
        [ del_codes.append(code) for code in current_codes \
            if code not in self.__physical_copies_container.get_physical_codes() ]
        # Dodaj wszystkie kody z add_codes
        for code in add_codes:
            PhysicalDVDModel.insert({
                'physical_code': code,
                'dvd_id': self.__dvd_id,
                'rental_state': DatabaseManager.RETURNED
            })
        # Usuń wszystkie wpisy z kodami z del_codes
        PhysicalDVDModel.delete_where({
            'dvd_id': self.__dvd_id,
            'physical_code': del_codes
        })

    def __delete_dvd(self):
        DVDModel.delete_where({'id': self.__dvd_id})
        messagebox.showinfo(title='DVD delete', message='Płyta usunięta pomyślnie!')
        self.__quit_view()

    def __quit_view(self):
        self.__controller.change_view('dvd_search')
