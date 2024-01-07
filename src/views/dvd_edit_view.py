import tkinter as tk
from tkinter import ttk
from src.database.models import DVDModel
from datetime import datetime

class DVDEditView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, width=parent.winfo_reqwidth())

        self.name_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.categories_var = tk.StringVar()
        self.physical_var = tk.StringVar()
        if controller.selected_dvd != -1:
            model = DVDModel.select({'id': controller.selected_dvd})[0]
            self.name_var.set(model.name)
            self.date_var.set(str(datetime.fromtimestamp(model.date).strftime("%d/%m/%Y")))

        container = ttk.Frame(self)
        container.pack(fill='x', expand=True, padx=(50,0), pady=(50,0))
        ttk.Label(container, text="Edycja płyty DVD", font=('Arial', 22)).pack(pady=(8,20))
        ttk.Button(container, text="Usuń płytę DVD").pack(anchor='e', pady=(0,20), padx=(0,40))
        # Pole do wpisania nazwy
        ttk.Label(container, text='Nazwa', font=('Arial', 16)).pack(anchor='w')
        ttk.Entry(container, textvariable=self.name_var, width=30).pack(anchor='w', pady=(8,20))
        # Pole do wpisania opisu
        ttk.Label(container, text='Opis', font=('Arial', 16)).pack(anchor='w')
        tk.Text(container, width=50, height=6).pack(anchor='w', pady=(8,20))
        # Pole do wpisania roku wydania
        ttk.Label(container, text='Rok wydania', font=('Arial', 16)).pack(anchor='w')
        ttk.Entry(container, textvariable=self.date_var, width=30).pack(anchor='w', pady=(8,20))
        # Pole do wpisania kategorii
        ttk.Label(container, text='Kategorie (wymień po przecinku)', font=('Arial', 16)).pack(anchor='w')
        ttk.Entry(container, width=30).pack(anchor='w', pady=(8,20))
        # Pole do wpisania kodów fizycznych kopii
        ttk.Label(container, text='Kody fizycznych kopii (wymień po przecinku)', font=('Arial', 16)).pack(anchor='w')
        ttk.Entry(container, width=30).pack(anchor='w', pady=(8,20))
        # Przycisk do stworzenia zapisu o płycie DVD
        ttk.Button(container, text='Aktualizuj').pack(anchor='w', padx=50, pady=10)
