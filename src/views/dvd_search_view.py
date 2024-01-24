from tkinter import ttk
import tkinter as tk
from datetime import datetime
from src.database.models import DVDModel
from src.frames import DVDFrame

class DVDSearchView(ttk.Frame):
    def __init__(self, parent, controler):
        super().__init__(parent)
        self.controler = controler
        self.selected_dvd = -1
        self.page = 1
        self.dvds_count = len(DVDModel.select())
        self.page_labels = []
        # -- Ttworzenie elementów widoku --
        self.dvd_frames = [] # aktualnie wyświetlane dvd_frame
        self.search_bar = self.create_search_bar() # tworzenie pola do wyszukiwania
        self.create_button_bar() # stworzenie przycisków do przełączania stron
        self.dvd_frames_container = ttk.Frame(self) # stworzenie kontenera na dvd_frame
        self.dvd_frames_container.pack(fill='x', padx=50) # wyświetlenie go
        self.create_search(self.dvd_frames_container) # wypełnienie kontenera 
        self.create_button_bar() # stworzenie kolejnych przycisków do przełączania stron
    
    def create_search_bar(self):
        sb = ttk.Frame(self) # stworzenie Frame na wszystkie elementy poniżej
        sb.pack(pady=10) # wyświetlenie go
        entry = ttk.Entry(sb, width=40) # stworzenie pola do wpisywania
        entry.pack(side='left') # wyświetlenie go
        submit = ttk.Button(sb, text="Submit", command=self.on_submit) # stworzenie przycisku Submit
        submit.pack(side='left', padx=10) # wyświetlenie go
        return sb

    # funkcja uruchamiana wciśnięciem przycisku Submit
    def on_submit(self):
        print("click :smile:")

    # wypełniane kontenera dvd_frames
    def create_search(self, parent):
        # usunięcie obiektów i wyczyszczenie tablicy
        for dvd_frame in self.dvd_frames:
            dvd_frame.destroy()
        self.dvd_frames = []
        # stworzenie nowych DVDFrame
        dvd_models = DVDModel.select(limit=10, offset=(self.page-1)*10)
        for i, dvd_model in enumerate(dvd_models):
            dvd = DVDFrame(parent, self, dvd_model)
            dvd.pack(anchor='w', pady=15, padx=10)
            self.dvd_frames.append(dvd)

    # tworzenie panelu z przyciskami do przełączania stron
    def create_button_bar(self):
        bottom_bar = ttk.Frame(self)
        left_button = ttk.Button(bottom_bar, text="<", command=self.prev_page)
        left_button.pack(side='left')
        page_label = ttk.Label(bottom_bar, text="1")
        self.page_labels.append(page_label)
        page_label.pack(padx=30, side='left')
        right_button = ttk.Button(bottom_bar, text=">", command=self.next_page)
        right_button.pack(side='left')
        bottom_bar.pack(pady=10)

    def dvd_borrow_view(self):
        self.controler.selected_dvd = self.selected_dvd
        self.controler.change_view('dvd_borrow')

    def dvd_edit_view(self):
        self.controler.selected_dvd = self.selected_dvd
        self.controler.change_view('dvd_edit')

    def next_page(self):
        print(self.dvds_count)
        if self.dvds_count - (self.page * 10) > 0:
            self.page += 1
            self.update_page()

    def prev_page(self):
        if self.page > 1:
            self.page -= 1
            self.update_page()

    def update_page(self):
        for label in self.page_labels:
            label.configure(text = str(self.page))
        self.create_search(self.dvd_frames_container)

