from tkinter import ttk
import tkinter as tk
from datetime import datetime
from src.database.models import DVDModel
from src.frames import DVDFrame

class DVDSearchView(ttk.Frame):
    def __init__(self, parent, controler):
        super().__init__(parent, width=parent.winfo_reqwidth())
        self.controler = controler
        self.selected_dvd = -1
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
        dvd_models = DVDModel.select(limit=10)
        for i, dvd_model in enumerate(dvd_models):
            dvd = DVDFrame(parent, self, dvd_model)
            dvd.pack(anchor='w', pady=15, padx=10)
            self.dvd_frames.append(dvd)

    # tworzenie panelu z przyciskami do przełączania stron
    def create_button_bar(self):
        bottom_bar = ttk.Frame(self)
        left_button = ttk.Button(bottom_bar, text="<")
        left_button.pack(side='left')
        ttk.Label(bottom_bar, text="1").pack(padx=30, side='left')
        right_button = ttk.Button(bottom_bar, text=">")
        right_button.pack(side='left')
        bottom_bar.pack(pady=10)

    def dvd_borrow_view(self):
        self.controler.selected_dvd = self.selected_dvd
        self.controler.change_view('dvd_borrow')

    def dvd_edit_view(self):
        self.controler.selected_dvd = self.selected_dvd
        self.controler.change_view('dvd_edit')

