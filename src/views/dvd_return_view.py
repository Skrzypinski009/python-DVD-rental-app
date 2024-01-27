import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from src.database.models import HistoryLogModel
from src.database.models import PhysicalDVDModel
from src.database.database_manager import DatabaseManager

class DVDReturnView(tk.Frame):
    def __init__(self, parent, controler):
        super().__init__(parent, bg='#555')
        self.__code_var = tk.StringVar()

        self.__create_view()

    def __create_view(self):
        tk.Label(self, text="Zwrot płyty", font=('Arial', 22), bg='#555', fg='white').pack(pady=20)
        tk.Label(
            self, text='Kod fizycznej kopii', bg='#555', fg='white', font=('Arial', 14)
        ).pack(pady=10, anchor='w', padx=(50,0))
        tk.Entry(self, textvariable=self.__code_var).pack(pady=10, anchor='w', padx=(50,0))
        tk.Button(
            self, text="Zwróć", command=self.__return_dvd,
            bg='#333', fg='white', activebackground='#444', activeforeground='white',
            highlightthickness=0, relief='flat', font=('Arial', 14)
        ).pack(anchor='w', padx=(50,0))
        self.__warning_label = tk.Label(self, text='', bg='#555', fg='white')
        self.__warning_label.pack(anchor='w')

    def __return_dvd(self):
        code = self.__code_var.get()
        p_dvd_rows = PhysicalDVDModel.select({'physical_code': code})
        if len(p_dvd_rows) == 0:
            self.__warning_label.configure(text='There is no DVD copy with this code!')
            return
        p_dvd = p_dvd_rows[0]
        
        history_log_rows = HistoryLogModel.select(
            {'physical_dvd_id': p_dvd.get_id()}, order_col='time_date', desc=True, limit=1
        )
        if len(history_log_rows) == 0:
            self.__warning_label.configure(text='This copy is not borrowed!')
            return 
        
        history_log = history_log_rows[0]
        if history_log.get_rental_state() == DatabaseManager.RETURNED:
            self.__warning_label.configure(text='This copy is not borrowed!')
            return 

        HistoryLogModel.insert({
            'time_date': datetime.now(),
            'physical_dvd_id': history_log.get_physical_dvd_id(),
            'rental_state': DatabaseManager.RETURNED,
            'client_id': history_log.get_client_id()
        })
        PhysicalDVDModel.select(
            {'id': history_log.get_physical_dvd_id()}
        )[0].update(
            {'rental_state': DatabaseManager.RETURNED}
        )
        messagebox.showinfo(title='DVD return', message='Płyta zwrócona pomyślnie!')
        self.__code_var.set('')

