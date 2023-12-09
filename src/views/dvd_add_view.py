import tkinter as tk
from tkinter import ttk

class DVDAddView(ttk.Frame):
    def __init__(self, parent, controler):
        super().__init__(parent, width=parent.winfo_reqwidth())
        container = ttk.Frame(self)
        container.pack(fill='x', expand=True, padx=(50,0), pady=(50,0))
        ttk.Label(container, text="Dodawanie nowej płyty DVD", font=('Arial', 22)).pack(anchor='w', pady=(8,20))
        # Pole do wpisania nazwy
        ttk.Label(container, text='Nazwa', font=('Arial', 16)).pack(anchor='w')
        ttk.Entry(container).pack(anchor='w', pady=(8,20))
        # Pole do wpisania opisu
        ttk.Label(container, text='Opis', font=('Arial', 16)).pack(anchor='w')
        ttk.Entry(container).pack(anchor='w', pady=(8,20))
        # Pole do wpisania roku wydania
        ttk.Label(container, text='Rok wydania', font=('Arial', 16)).pack(anchor='w')
        ttk.Entry(container).pack(anchor='w', pady=(8,20))
        # Pole do wpisania kategorii
        ttk.Label(container, text='Kategorie (wymień po przecinku)', font=('Arial', 16)).pack(anchor='w')
        ttk.Entry(container).pack(anchor='w', pady=(8,20))
        # Pole do wpisania kodów fizycznych kopii
        ttk.Label(container, text='Kody fizycznych kopii (wymień po przecinku)', font=('Arial', 16)).pack(anchor='w')
        ttk.Entry(container).pack(anchor='w', pady=(8,20))
        # Przycisk do stworzenia zapisu o płycie DVD
        ttk.Button(container, text='Stwórz').pack(anchor='w', padx=50, pady=10)
