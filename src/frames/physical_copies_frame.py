import tkinter as tk
from tkinter import ttk
from src.database.models import PhysicalDVDModel
from src.frames.physical_remove_frame import PhysicalRemoveFrame

class PhysicalCopiesFrame(ttk.Frame):
    def __init__(self, parent, controller, dvd_id):
        super().__init__(parent)
        self.controller = controller
        self.dvd_id = dvd_id
        self.physical_codes = []
        self.code_var = tk.StringVar()

        self.create_frame()
        

    def create_frame(self):
        # Kody fizycznych kopii
        self.copy_container = ttk.Frame(self)
        self.copy_container.pack()
        ttk.Label(self.copy_container, text='Kody fizycznych kopii', font=('Arial', 16)).pack(anchor='w')
        physical_dvds = PhysicalDVDModel.select({'dvd_id': self.dvd_id})
        for physical in physical_dvds:
            code = physical.get_physical_code()
            PhysicalRemoveFrame(self.copy_container, self, code).pack(anchor='w', padx=30)
            self.physical_codes.append(code)
        # Dodawanie nowego kodu
        add_copy_container = ttk.Frame(self)
        add_copy_container.pack(pady=(30, 0))
        ttk.Entry(add_copy_container, textvariable=self.code_var).pack(side='left', padx=20)
        ttk.Button(add_copy_container, text='Dodaj', command=self.add_code).pack(side='left')
        # Wyświetlanie ostrzeżeń
        self.code_warning_label = ttk.Label(self, text='')
        self.code_warning_label.pack()

    def del_code(self, code):
        if code in self.physical_codes:
            self.physical_codes.remove(code)

    def add_code(self):
        code = self.code_var.get()
        # Wyświetlanie błędów
        if len(code) != 5:
            self.code_warning_label.configure(text='Code should be 5 characters long!')
            return
        if len(PhysicalDVDModel.select({'physical_code': code})) != 0:
            self.code_warning_label.configure(text='This code already exist!')
            return
        # Dodanie kodu do interfejsu
        PhysicalRemoveFrame(self.copy_container, self, code).pack(anchor='w', padx=30)
        self.physical_codes.append(code)
        # Wyczyszczenie pola i informacja o dodaniu kodu
        self.code_var.set('')
        self.code_warning_label.configure(text='')
