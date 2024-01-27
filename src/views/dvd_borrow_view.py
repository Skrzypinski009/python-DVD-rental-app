import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from src.database.database_manager import DatabaseManager
from src.database.models import ClientModel
from src.database.models import PhysicalDVDModel
from src.database.models import HistoryLogModel

class DVDBorrowView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='#555')
        self.__bg_color = '#555'
        self.__dvd_id = controller.get_selected_dvd_id()
        self.__controller = controller

        self.__name_var = tk.StringVar()
        self.__last_name_var = tk.StringVar()
        self.__email_var = tk.StringVar()
        self.__phone_var = tk.StringVar()
        self.__physical_code_var = tk.StringVar()
        self.__create_view()

    def __create_view(self):
        container = tk.Frame(self, bg=self.__bg_color)
        container.pack(padx=(50,0), pady=50)
        tk.Label(
            container, text="Wyporzyczanie pozycji", font=('Arial', 22),
            bg=self.__bg_color, fg='white'
        ).pack(pady=20, padx=20)
        tk.Label(
            container, text='Dane Klijenta', font=('Arial', 18),
            bg=self.__bg_color, fg='white'
        ).pack(anchor='w',pady=20, padx=20)
# pole imie
        tk.Label(
            container, text='Imie: ', font=('Arial',14),
            bg=self.__bg_color, fg='white'
        ).pack(anchor='w',padx=50)
        tk.Entry(container, width=40, textvariable=self.__name_var).pack(anchor='w', padx=70)    
# pole nazwisko
        tk.Label(
            container, text='Nazwisko: ', font=('Arial',14),
            bg=self.__bg_color, fg='white'
        ).pack(anchor='w', padx=50)
        tk.Entry(container, width=40, textvariable=self.__last_name_var).pack(anchor='w', padx=70)    
# pole email
        tk.Label(
            container, text='E-mail: ', font=('Arial',14),
            bg=self.__bg_color, fg='white'
        ).pack(anchor='w', padx=50)
        tk.Entry(container, width=40, textvariable=self.__email_var).pack(anchor='w', padx=70)    
# pole nr tel
        tk.Label(
            container, text='Numer telefonu: ', font=('Arial',14),
            bg=self.__bg_color, fg='white'
         ).pack(anchor='w', padx=50)
        tk.Entry(container, width=40, textvariable=self.__phone_var).pack(anchor='w', padx=70)    
# Kod kopii
        tk.Label(
            container, text='Dane DVD', font=('Arial', 18),
            bg=self.__bg_color, fg='white'
         ).pack(anchor='w',pady=20, padx=20)
        tk.Label(
            container, text="Kody dla tej płyty:", font=('Arial', 14),
            bg=self.__bg_color, fg='white'
         ).pack(anchor='w', padx=70)
#Wyświetlenie kodów dla danej płyty
        codes_container = tk.Frame(container, bg=self.__bg_color)
        codes_container.pack()
        rows = PhysicalDVDModel.select({'dvd_id': self.__dvd_id})
        print(rows)
        for row in rows:
            code_frame = tk.Frame(codes_container, bg=self.__bg_color)
            code_frame.pack(pady=5)
            tk.Label(
                code_frame, text=row.get_physical_code(), width=7,
                bg='#aa5555', fg='white'
            ).pack(side='left')
            tk.Label(
                code_frame, 
                text='wyporzyczone' if row.get_rental_state() == DatabaseManager.BORROWED else 'niewypożyczone',
                width=15,
                bg='#aa5555', fg='white'
            ).pack(side='left')
# Pole kodu kopii
        tk.Label(
            container, text='Kod kopi: ', font=('Arial',14),
            bg=self.__bg_color, fg='white'
        ).pack(anchor='w', padx=50)
        tk.Entry(container, width=40, textvariable=self.__physical_code_var).pack(anchor='w', padx=70)   
# Potwierdzenie
        tk.Button(container, text='Wypożycz', command=self.__borrow).pack(anchor='w', padx=10, pady=25) 
        self.__warning_label = tk.Label(container, text='', bg=self.__bg_color, fg='white')
        self.__warning_label.pack(pady=20)

    def __borrow(self):
        name = self.__name_var.get()
        last_name = self.__last_name_var.get()
        email = self.__email_var.get()
        phone = self.__phone_var.get()
        physical_code = self.__physical_code_var.get()

        if name == '' or last_name == '' or email == '' or phone == '' or physical_code == '':
            self.__warning_label.configure(text='Wypełnij wszystkie pola!')
            return

        # Sprawdzanie kodu kopii
        p_dvd_rows = PhysicalDVDModel.select({
            'physical_code': physical_code, 'dvd_id': self.__dvd_id
        })
        if len(p_dvd_rows) == 0:
            self.__warning_label.configure(text=f"Ta płyta nie posiada kopii z kodem {physical_code}.")
            return
        elif len(p_dvd_rows) != 0 and p_dvd_rows[0].get_rental_state() == DatabaseManager.BORROWED:
            self.__warning_label.configure(text=f"Ta kopia jest już wypożyczona ({physical_code}).")
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

        messagebox.showinfo(title='DVD borrow', message='Płyta wypożyczona pomyślnie!')
        self.__controller.change_view('dvd_search')

