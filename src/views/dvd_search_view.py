from tkinter import ttk
import tkinter as tk

class DVDSearchView(ttk.Frame):
    def __init__(self, parent, controler):
        super().__init__(parent, width=parent.winfo_reqwidth())
        # -- Ttworzenie elementów widoku --
        self.dvd_frames = [] # aktualnie wyświetlane dvd_frame
        self.search_bar = self.create_search_bar() # tworzenie pola do wyszukiwania
        self.create_button_bar() # stworzenie przycisków do przełączania stron
        self.dvd_frames_container = ttk.Frame(self) # stworzenie kontenera na dvd_frame
        self.dvd_frames_container.pack(fill='x', padx=50) # wyświetlenie go
        self.create_search() # wypełnienie kontenera 
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
    def create_search(self):
        # usunięcie obiektów i wyczyszczenie tablicy
        for dvd_frame in self.dvd_frames:
            dvd_frame.destroy()
        self.dvd_frames = []
        # stworzenie nowych obiektów
        for i in range(10):
            dvd = self.create_dvd_frame()
            self.dvd_frames.append(dvd)

    # stworzenie dvd_frame reprezentującego jeden film
    def create_dvd_frame(self):
        dvd_frame = tk.Frame(self.dvd_frames_container, borderwidth=3, relief='solid')
        # anchor='w' znaczy że przyczepia się do lewej krawędzi
        dvd_frame.pack(anchor='w', pady=15, padx=10)
        ttk.Label(dvd_frame, text="Tytuł filmu").pack(anchor='w')
        ttk.Label(dvd_frame, text="Opis filmu").pack(anchor='w')
        ttk.Label(dvd_frame, text="Rok wydania").pack(anchor='w')
        cat_frame = ttk.Frame(dvd_frame)
        cat_frame.pack(anchor='w')
        for i in range(4): # tworzenie poglądowych kategorii
            lab = ttk.Label(cat_frame, text="Category")
            lab.pack(padx=10, side='left')
        ttk.Label(dvd_frame, text="liczba kopii: 2").pack(anchor='w')
        return dvd_frame

    # tworzenie panelu z przyciskami do przełączania stron
    def create_button_bar(self):
        bottom_bar = ttk.Frame(self)
        left_button = ttk.Button(bottom_bar, text="<")
        left_button.pack(side='left')
        ttk.Label(bottom_bar, text="1").pack(padx=30, side='left')
        right_button = ttk.Button(bottom_bar, text=">")
        right_button.pack(side='left')
        bottom_bar.pack(pady=10)

