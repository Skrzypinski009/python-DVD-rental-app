import tkinter as tk
from tkinter import ttk
from datetime import datetime
from src.database.models import DVDModel
from src.database.models import CategoryModel
from src.frames import CategoryCheckboxFrame

class DVDAddView(ttk.Frame):
    def __init__(self, parent, controler):
        super().__init__(parent, width=parent.winfo_reqwidth())
        med_font = ('Arial', 16)

        self.name_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.container = ttk.Frame(self)

        self.categories_frames = []
        self.container.pack(fill='x', expand=True, padx=(50,0), pady=(50,0))

        ttk.Label(self.container, text="Dodawanie nowej płyty DVD", font=('Arial', 22)).pack(pady=(8,20))
        # Pole do wpisania nazwy
        ttk.Label(self.container, text='Nazwa', font=med_font).pack(anchor='w')
        ttk.Entry(self.container, width=30, textvariable=self.name_var).pack(anchor='w', pady=(8,20))
        # Pole do wpisania opisu
        ttk.Label(self.container, text='Opis', font=med_font).pack(anchor='w')
        tk.Text(self.container, width=50, height=6).pack(anchor='w', pady=(8,20))
        # Pole do wpisania roku wydania
        ttk.Label(self.container, text='Rok wydania (DDMMYYY)', font=med_font).pack(anchor='w')
        ttk.Entry(self.container, width=30, textvariable=self.date_var).pack(anchor='w', pady=(8,20))
        # Pole do wpisania kategorii
        ttk.Label(self.container, text='Kategorie (wymień po przecinku)', font=med_font).pack(anchor='w')
        for cat in CategoryModel.select():
            cat_frame = CategoryCheckboxFrame(self.container, self, cat.name)
            cat_frame.pack(anchor='w', pady=(8,20))
            categories_frames.append(cat_frame)

        ttk.Entry(self.container, width=30).pack(anchor='w', pady=(8,20))
        # Pole do wpisania kodów fizycznych kopii
        ttk.Label(self.container, text='Kody fizycznych kopii (wymień po przecinku)', font=med_font).pack(anchor='w')
        ttk.Entry(self.container, width=30).pack(anchor='w', pady=(8,20))
        # Przycisk do stworzenia zapisu o płycie DVD
        ttk.Button(self.container, text='Stwórz', command=self.add_dvd).pack(anchor='w', padx=50, pady=10)
        self.message_label = ttk.Label(self.container, text="", font=('Arial', 12))
        self.message_label.pack()

    def add_dvd(self):
        name = self.name_var.get(),
        date = datetime.strptime(self.date_var.get(), "%d/%m/%Y").timestamp()
        if(len(DVDModel.select(name=name, date=date)) != 0):
            self.message_label.config(text="This dvd is already existing!")

        categories = self.categories_var.get().split(',')
        categories = [cat.strip() for cat in categories]
        category_models = []
        for cat in categories:
            pass

        DVDModel.insert(name, date)
        self.message_label.config(text="DVD added successfuly!")
        dvd_model = DVDModel.get_by_row(DVDModel.select(name=name, date=date)[0])

