import tkinter as tk
from tkinter import ttk
from datetime import datetime
from src.database.models import HistoryLogModel
from src.database.models import PhysicalDVDModel
from src.database.models import ClientModel
from src.database.database_manager import DatabaseManager


class HistoryLogView(ttk.Frame):
    def __init__(self, parent, controler):
        super().__init__(parent)
        self.log_frames = []
        self.page = 1
        self.history_log_count = len(HistoryLogModel.select())
        self.page_labels = []

        self.search_bar = self.create_search_bar()
        self.create_button_bar()
        self.log_frames_container = ttk.Frame(self)
        self.log_frames_container.pack(fill='x', padx=50)
        self.create_search()
        self.create_button_bar()
                
    def create_search_bar(self):
        sb = ttk.Frame(self) # stworzenie Frame na wszystkie elementy poniżej
        sb.pack(pady=10) # wyświetlenie go
        entry = ttk.Entry(sb, width=40) # stworzenie pola do wpisywania
        entry.pack(side='left') # wyświetlenie go
        submit = ttk.Button(sb, text="Submit", command=self.on_submit) # stworzenie przycisku Submit
        submit.pack(side='left', padx=10) # wyświetlenie go
        return sb

    def create_button_bar(self):
        bottom_bar = ttk.Frame(self)
        left_button = ttk.Button(bottom_bar, text="<", command=self.prev_page)
        left_button.pack(side='left')
        page_label = ttk.Label(bottom_bar, text="1")
        page_label.pack(padx=30, side='left')
        self.page_labels.append(page_label)
        right_button = ttk.Button(bottom_bar, text=">", command=self.next_page)
        right_button.pack(side='left')
        bottom_bar.pack(pady=20)

    def on_submit(self):
        print("click :smile:")

    def create_search(self):
        # usunięcie obiektów i wyczyszczenie tablicy
        for log_frame in self.log_frames:
            log_frame.destroy()
        self.dvd_frames = []
        # stworzenie nowych obiektów
        history_log_rows = HistoryLogModel.select(offset=(self.page-1)*30, limit=30, order_col='time_date', desc=True)
        for history_log in history_log_rows:
            log = self.create_log_frame(history_log)
            self.dvd_frames.append(log)

    def create_log_frame(self, history_log):
        client_id = history_log.get_client_id()
        client = ClientModel.select({'id': client_id})[0]
        name = client.get_first_name()
        last_name = client.get_last_name()
        email = client.get_email()
        phone = client.get_phone_number()
        rental_state = 'wypożyczenie' if history_log.get_rental_state() == DatabaseManager.BORROWED else 'zwrot'
        code = PhysicalDVDModel.select({'id': history_log.get_physical_dvd_id()})[0].get_physical_code()
        date = datetime.fromtimestamp(history_log.get_time_date()).strftime("%d/%m/%Y %H:%M")
        log_frame = ttk.Frame(self.log_frames_container)
        log_frame.pack(pady=(20, 0))
        ttk.Label(log_frame, text=rental_state, width=15).pack(padx=10, side='left')
        ttk.Label(log_frame, text=name, width=15).pack(padx=10, side='left')
        ttk.Label(log_frame, text=last_name, width=15).pack(padx=10, side='left')
        ttk.Label(log_frame, text=phone, width=20).pack(padx=10, side='left')
        ttk.Label(log_frame, text=email, width=25).pack(padx=10, side='left')
        ttk.Label(log_frame, text=code, width=5).pack(padx=10, side='left')
        ttk.Label(log_frame, text=date, width=15).pack(padx=10, side='left')
        return log_frame

    def next_page(self):
        if self.history_log_count - self.page * 30 > 0:
            self.page += 1
            self.update_page()

    def prev_page(self):
        if self.page > 1:
            self.page -= 1
            self.update_page()

    
    def update_page(self):
        for label in self.page_labels:
            label.configure(text=str(self.page))
        self.create_search()

