import tkinter as tk
from datetime import datetime
from src.database.models import HistoryLogModel
from src.database.models import PhysicalDVDModel
from src.database.models import ClientModel
from src.database.database_manager import DatabaseManager


class HistoryLogView(tk.Frame):
    def __init__(self, parent, controler):
        super().__init__(parent, bg='#555')
        self.__bg_color = '#555'
        self.__log_frames = []
        self.__page = 1
        self.__history_log_count = len(HistoryLogModel.select())
        self.__page_labels = []
        self.__create_view()

    def __create_view(self):
        self.__create_button_bar()
        self.__log_frames_container = tk.Frame(self, bg=self.__bg_color)
        self.__log_frames_container.pack(fill='x', padx=50)
        self.__create_search()
        self.__create_button_bar()

    def __create_button_bar(self):
        bottom_bar = tk.Frame(self, bg=self.__bg_color)
        left_button = tk.Button(
            bottom_bar, text="<", command=self.__prev_page, width=3,
            bg='#333', fg='white', activebackground='#444', activeforeground='white',
            highlightthickness=0, relief='flat'
         )
        left_button.pack(side='left')
        page_label = tk.Label(bottom_bar, text="1", bg=self.__bg_color, fg='white', font=('Arial', 16))
        self.__page_labels.append(page_label)
        page_label.pack(padx=30, side='left')
        right_button = tk.Button(
            bottom_bar, text=">", command=self.__next_page, width=3,
            bg='#333', fg='white', activebackground='#444', activeforeground='white',
            highlightthickness=0, relief='flat'
         )
        right_button.pack(side='left')
        bottom_bar.pack(pady=10)

    def __create_search(self):
        # usunięcie obiektów i wyczyszczenie tablicy
        for log_frame in self.__log_frames:
            log_frame.destroy()
        self.__dvd_frames = []
        # stworzenie nowych obiektów
        history_log_rows = HistoryLogModel.select(offset=(self.__page-1)*30, limit=30, order_col='time_date', desc=True)
        for history_log in history_log_rows:
            log = self.__create_log_frame(history_log)
            self.__dvd_frames.append(log)

    def __create_log_frame(self, history_log):
        client_id = history_log.get_client_id()
        client = ClientModel.select({'id': client_id})[0]
        name = client.get_first_name()
        last_name = client.get_last_name()
        email = client.get_email()
        phone = client.get_phone_number()
        rental_state = 'wypożyczenie' if history_log.get_rental_state() == DatabaseManager.BORROWED else 'zwrot'
        code = PhysicalDVDModel.select({'id': history_log.get_physical_dvd_id()})[0].get_physical_code()
        date = datetime.fromtimestamp(history_log.get_time_date()).strftime("%d/%m/%Y %H:%M")
        log_frame = tk.Frame(self.__log_frames_container, bg='#555', highlightthickness=2, highlightbackground='black')
        log_frame.pack(pady=(20, 0))
        tk.Label(
            log_frame, text=rental_state, width=15,
            bg=self.__bg_color, fg='white',
            font=('Arial', 12),
        ).pack(padx=10, side='left')
        tk.Label(
            log_frame, text=name, width=15,
            bg=self.__bg_color, fg='white',
            font=('Arial', 12),
        ).pack(padx=10, side='left')
        tk.Label(
            log_frame, text=last_name, width=15,
            bg=self.__bg_color, fg='white',
            font=('Arial', 12),
        ).pack(padx=10, side='left')
        tk.Label(
            log_frame, text=phone, width=20,
            bg=self.__bg_color, fg='white',
            font=('Arial', 12),
        ).pack(padx=10, side='left')
        tk.Label(
            log_frame, text=email, width=25,
            bg=self.__bg_color, fg='white',
            font=('Arial', 12),
        ).pack(padx=10, side='left')
        tk.Label(
            log_frame, text=code, width=5,
            bg=self.__bg_color, fg='white',
            font=('Arial', 12),
        ).pack(padx=10, side='left')
        tk.Label(
            log_frame, text=date, width=15,
            bg=self.__bg_color, fg='white',
            font=('Arial', 12),
        ).pack(padx=10, side='left')
        return log_frame

    def __next_page(self):
        if self.__history_log_count - self.__page * 30 > 0:
            self.__page += 1
            self.__update_page()

    def __prev_page(self):
        if self.__page > 1:
            self.__page -= 1
            self.__update_page()

    
    def __update_page(self):
        for label in self.__page_labels:
            label.configure(text=str(self.__page))
        self.__create_search()

