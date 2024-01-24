import tkinter as tk
from tkinter import ttk
from random import randrange

class HistoryLogView(ttk.Frame):
    def __init__(self, parent, controler):
        super().__init__(parent)
        self.log_frames = []
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
        left_button = ttk.Button(bottom_bar, text="<")
        left_button.pack(side='left')
        ttk.Label(bottom_bar, text="1").pack(padx=30, side='left')
        right_button = ttk.Button(bottom_bar, text=">")
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
        for i in range(30):
            log = self.create_log_frame(i)
            self.dvd_frames.append(log)

    def create_log_frame(self, idx):
        name = self.get_random_name()
        last_name = self.get_random_lastname()
        log_frame = ttk.Frame(self.log_frames_container)
        log_frame.pack(pady=(20, 0))
        ttk.Label(log_frame, text=self.get_random_rental_state(), width=15).pack(padx=10, side='left')
        ttk.Label(log_frame, text=name, width=15).pack(padx=10, side='left')
        ttk.Label(log_frame, text=last_name, width=15).pack(padx=10, side='left')
        ttk.Label(log_frame, text="+48 888 777 444", width=20).pack(padx=10, side='left')
        ttk.Label(
            log_frame, 
            text="{}{}@poczta.pl".format(name.lower(), last_name.lower()), 
            width=25
        ).pack(padx=10, side='left')
        ttk.Label(log_frame, text="Y76U3A1", width=15).pack(padx=10, side='left')
        return log_frame

    def get_random_rental_state(self):
        return "Wypożyczenie" if randrange(0,2) == 0 else "Zwrot"

    def get_random_name(self):
        names = ['Marek', 'Jan', 'Kamil', 'Bogdan', 'Freddy']
        return names[randrange(0,len(names))]

    def get_random_lastname(self):
        last_names = ['Kowalski', 'Wielki', 'Stopa', 'Fazbear', 'Szybcior']
        return last_names[randrange(0,len(last_names))]



