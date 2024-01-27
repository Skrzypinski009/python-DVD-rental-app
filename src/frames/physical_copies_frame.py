import tkinter as tk
from tkinter import ttk
from src.database.models import PhysicalDVDModel
from src.frames.physical_remove_frame import PhysicalRemoveFrame

class PhysicalCopiesFrame(tk.Frame):
    def __init__(self, parent, controller, dvd_id):
        super().__init__(parent, bg='#555')
        self.__dvd_id = dvd_id
        self.__physical_codes = []
        self.__code_var = tk.StringVar()

        self.__create_frame()
        
    def get_physical_codes(self):
        return self.__physical_codes

    def __create_frame(self):
        # Kody fizycznych kopii
        self.__copy_container = tk.Frame(self, bg='#555')
        self.__copy_container.pack()
        tk.Label(
            self.__copy_container, text='Kody fizycznych kopii', font=('Arial', 16),
            bg='#555', fg='white'
        ).pack(anchor='w')
        physical_dvds = PhysicalDVDModel.select({'dvd_id': self.__dvd_id})
        for physical in physical_dvds:
            code = physical.get_physical_code()
            PhysicalRemoveFrame(self.__copy_container, self, code).pack(anchor='w', padx=30)
            self.__physical_codes.append(code)
        # Dodawanie nowego kodu
        add_copy_container = tk.Frame(self, bg='#555')
        add_copy_container.pack(pady=(30, 0))
        ttk.Entry(add_copy_container, textvariable=self.__code_var).pack(side='left', padx=20)
        ttk.Button(add_copy_container, text='Dodaj', command=self.__add_code).pack(side='left')
        # Wyświetlanie ostrzeżeń
        self.__code_warning_label = tk.Label(self, text='', bg='#555')
        self.__code_warning_label.pack()

    def __add_code(self):
        code = self.__code_var.get()
        # Wyświetlanie błędów
        if len(code) != 5:
            self.__code_warning_label.configure(text='Code should be 5 characters long!')
            return
        if len(PhysicalDVDModel.select({'physical_code': code})) != 0:
            self.__code_warning_label.configure(text='This code already exist!')
            return
        # Dodanie kodu do interfejsu
        PhysicalRemoveFrame(self.__copy_container, self, code).pack(anchor='w', padx=30)
        self.__physical_codes.append(code)
        # Wyczyszczenie pola i informacja o dodaniu kodu
        self.__code_var.set('')
        self.__code_warning_label.configure(text='')

    def del_code(self, code):
        if code in self.__physical_codes:
            self.__physical_codes.remove(code)
