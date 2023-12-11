import tkinter as tk
from tkinter import ttk

class DVDReturnView(ttk.Frame):
    def __init__(self, parent, controler):
        super().__init__(parent, width=parent.winfo_reqwidth())
        ttk.Label(self, text="Zwrot płyty", font=('Arial', 22)).pack(pady=20)
        ttk.Label(self, text='Kod fizycznej kopii').pack(pady=10, anchor='w', padx=(50,0))
        ttk.Entry(self).pack(pady=10, anchor='w', padx=(50,0))
        ttk.Button(self, text="Zwróć").pack(anchor='w', padx=(50,0))

