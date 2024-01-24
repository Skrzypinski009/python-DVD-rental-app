import tkinter as tk
from tkinter import ttk
from datetime import datetime
from src.database.models import HistoryLogModel
from src.database.models import PhysicalDVDModel
from src.database.database_manager import DatabaseManager

class DVDReturnView(ttk.Frame):
    def __init__(self, parent, controler):
        super().__init__(parent)
        self.code_var = tk.StringVar()

        self.create_view()

    def create_view(self):
        ttk.Label(self, text="Zwrot płyty", font=('Arial', 22)).pack(pady=20)
        ttk.Label(self, text='Kod fizycznej kopii').pack(pady=10, anchor='w', padx=(50,0))
        ttk.Entry(self, textvariable=self.code_var).pack(pady=10, anchor='w', padx=(50,0))
        ttk.Button(self, text="Zwróć", command=self.return_dvd).pack(anchor='w', padx=(50,0))
        self.warning_label = ttk.Label(self, text='')
        self.warning_label.pack(anchor='w')

    def return_dvd(self):
        code = self.code_var.get()
        p_dvd_rows = PhysicalDVDModel.select({'physical_code': code})
        if len(p_dvd_rows) == 0:
            self.warning_label.configure(text='There is no DVD copy with this code!')
            return
        p_dvd = p_dvd_rows[0]
        
        history_log_rows = HistoryLogModel.select(
            {'physical_dvd_id': p_dvd.get_id()}, order_col='time_date', desc=True, limit=1
        )
        if len(history_log_rows) == 0:
            self.warning_label.configure(text='This copy is not borrowed!')
            return 
        
        history_log = history_log_rows[0]
        if history_log.get_rental_state() == DatabaseManager.RETURNED:
            self.warning_label.configure(text='This copy is not borrowed!')
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
        self.warning_label.configure(text='Returned Successfully!')
        self.code_var.set('')

