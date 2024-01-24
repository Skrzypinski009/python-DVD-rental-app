import tkinter as tk
from tkinter import ttk 
from datetime import datetime
import time
from src.database.database_manager import DatabaseManager
from src.database.models import ClientModel
from src.database.models import PhysicalDVDModel
from src.database.models import HistoryLogModel

class DVDBorrowView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.dvd_id = controller.selected_dvd
        self.controller = controller

        self.name_var = tk.StringVar()
        self.last_name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.physical_code_var = tk.StringVar()

        container = ttk.Frame(self)
        container.pack(padx=(50,0), pady=50)
        ttk.Label(container, text="Wyporzyczanie pozycji", font=('Arial', 22)).pack(pady=20, padx=20)
        ttk.Label(container, text='Dane Klijenta', font=('Arial', 18)).pack(anchor='w',pady=20, padx=20)
# pole imie
        ttk.Label(container, text='Imie: ', font=('Arial',14)).pack(anchor='w',padx=50)
        ttk.Entry(container, width=40, textvariable=self.name_var).pack(anchor='w', padx=70)    
# pole nazwisko
        ttk.Label(container, text='Nazwisko: ', font=('Arial',14)).pack(anchor='w', padx=50)
        ttk.Entry(container, width=40, textvariable=self.last_name_var).pack(anchor='w', padx=70)    
# pole email
        ttk.Label(container, text='E-mail: ', font=('Arial',14)).pack(anchor='w', padx=50)
        ttk.Entry(container, width=40, textvariable=self.email_var).pack(anchor='w', padx=70)    
# pole nr tel
        ttk.Label(container, text='Numer telefonu: ', font=('Arial',14)).pack(anchor='w', padx=50)
        ttk.Entry(container, width=40, textvariable=self.phone_var).pack(anchor='w', padx=70)    
# Kod kopii
        ttk.Label(container, text='Dane DVD', font=('Arial', 18)).pack(anchor='w',pady=20, padx=20)
        ttk.Label(container, text="Kody dla tej płyty:", font=('Arial', 14)).pack(anchor='w', padx=70)
#Wyświetlenie kodów dla danej płyty
        codes_container = ttk.Frame(container)
        codes_container.pack()
        rows = PhysicalDVDModel.select({'dvd_id': self.dvd_id})
        print(rows)
        for row in rows:
            code_frame = ttk.Frame(codes_container)
            code_frame.pack()
            ttk.Label(code_frame, text=row.get_physical_code(), width=7).pack(side='left')
            ttk.Label(
                code_frame, 
                text='wyporzyczone' if row.get_rental_state() == DatabaseManager.BORROWED else 'niewyporzyczone',
                width=15
            ).pack(side='left')
# Pole kodu kopii
        ttk.Label(container, text='Kod kopi: ', font=('Arial',14)).pack(anchor='w', padx=50)
        ttk.Entry(container, width=40, textvariable=self.physical_code_var).pack(anchor='w', padx=70)   
# Potwierdzenie
        ttk.Button(container, text='Wyporzycz', command=self.borrow).pack(anchor='w', padx=10, pady=25) 
        self.warning_label = ttk.Label(container, text='')
        self.warning_label.pack(pady=20)

    def borrow(self):
        name = self.name_var.get()
        last_name = self.last_name_var.get()
        email = self.email_var.get()
        phone = self.phone_var.get()
        physical_code = self.physical_code_var.get()

        if name == '' or last_name == '' or email == '' or phone == '' or physical_code == '':
            self.warning_label.configure(text='Fill all fields first!')
            return

        # Sprawdzanie kodu kopii
        p_dvd_rows = PhysicalDVDModel.select({
            'physical_code': physical_code, 'dvd_id': self.dvd_id
        })
        if len(p_dvd_rows) == 0:
            self.warning_label.configure(text=f"This dvd don't have code {physical_code}.")
            return
        elif len(p_dvd_rows) != 0 and p_dvd_rows[0].get_rental_state() == DatabaseManager.BORROWED:
            self.warning_label.configure(text=f"This copy is already borrowed ({physical_code}).")
            return
        p_dvd = p_dvd_rows[0]

        # Sprawdzanie klienta
        client_rows = ClientModel.select(
            {'first_name': name, 'last_name': last_name, 'email': email, 'phone_number': phone}
        )
        if len(client_rows) == 0:
            ClientModel.insert(
                {'first_name': name, 'last_name': last_name, 'email': email, 'phone_number': phone}
            )
            client_rows = ClientModel.select(
                {'first_name': name, 'last_name': last_name, 'email': email, 'phone_number': phone}
            )
        client = client_rows[0]

        date = datetime.now()

        HistoryLogModel.insert({
            'time_date': date, 
            'physical_dvd_id': p_dvd.get_id(), 
            'rental_state': DatabaseManager.BORROWED,
            'client_id': client.get_id()
        })
        p_dvd.update({'rental_state': DatabaseManager.BORROWED})

        self.warning_label.configure(text='Wyporzyczono pomyślnie')
        #TODO zmienić widok
        time.sleep(2)
        self.controller.change_view('dvd_search')

