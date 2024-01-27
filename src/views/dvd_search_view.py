from tkinter import ttk
import tkinter as tk
from datetime import datetime
from src.database.models import DVDModel
from src.database.models import CategoryModel
from src.database.database_manager import DatabaseManager
from src.frames import DVDFrame

class DVDSearchView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, background='#555')
        self.__bg_color = '#555'
        self.__controller = controller
        self.__selected_dvd = -1
        self.__page = 1
        self.__dvds_count = len(DVDModel.select())
        self.__page_labels = []
        self.__search_bar_var = tk.StringVar()
        self.__search = ''
        self.__dvd_frames = [] # aktualnie wyświetlane dvd_frame
        self.__create_view()

    def __create_view(self):
        self.__search_bar = self.__create_search_bar() # tworzenie pola do wyszukiwania
        self.__create_button_bar() # stworzenie przycisków do przełączania stron
        self.__dvd_frames_container = tk.Frame(self, background=self.__bg_color) # stworzenie kontenera na dvd_frame
        self.__dvd_frames_container.pack() # wyświetlenie go
        self.__create_search(self.__dvd_frames_container) # wypełnienie kontenera 
        self.__create_button_bar() # stworzenie kolejnych przycisków do przełączania stron

    def get_selected_dvd_id(self):
        return self.__selected_dvd

    def set_selected_dvd_id(self, dvd_id):
        self.__selected_dvd = dvd_id

    def __create_search_bar(self):
        sb = tk.Frame(self, background=self.__bg_color) # stworzenie Frame na wszystkie elementy poniżej
        sb.pack(pady=10) # wyświetlenie go
        entry = tk.Entry(sb, width=40, textvariable=self.__search_bar_var) # stworzenie pola do wpisywania
        entry.pack(side='left') # wyświetlenie go
        submit = tk.Button(
            sb, text="Submit", command=self.__on_submit, font=('Arial', 14),
            bg='#333', fg='white', activebackground='#444', activeforeground='white',
            highlightthickness=0, relief='flat'
        ) # stworzenie przycisku Submit
        submit.pack(side='left', padx=10) # wyświetlenie go
        return sb

    # funkcja uruchamiana wciśnięciem przycisku Submit
    def __on_submit(self):
        self.__search = self.__search_bar_var.get()
        self.__page = 1
        self.__update_page()

    # wypełniane kontenera dvd_frames
    def __create_search(self, parent):
        # usunięcie obiektów i wyczyszczenie tablicy
        for dvd_frame in self.__dvd_frames:
            dvd_frame.destroy()
        self.__dvd_frames = []
        #wyszukiwanie filmów
        like_dvd = {}
        where = {}
        
        if self.__search != '':
            splitted = self.__search.split(' ')
            like_dvd = { 'name': [ f"%{s}%" for s in splitted ] }
            like_category = { 'name': [ f"%{s}%" for s in splitted ]}
            categories = CategoryModel.select(like_fields=like_category)
            dvd_ids_raw = DatabaseManager.select(
                'dvd_category_relation', 
                ['dvd_id'],
                {'category_id': [ cat.get_id() for cat in categories ]},
                distinct = True
            )
            where = {'id': [ dvd[0] for dvd in dvd_ids_raw ]}

        # stworzenie nowych DVDFrame
        self.__dvds_count = len(DVDModel.select(
            where, like_fields=like_dvd))

        dvd_models = DVDModel.select(
            where,
            limit=10, 
            offset=(self.__page-1)*10, 
            like_fields=like_dvd
        )
        for i, dvd_model in enumerate(dvd_models):
            dvd = DVDFrame(parent, self, dvd_model)
            dvd.pack(pady=15, padx=10)
            self.__dvd_frames.append(dvd)

    # tworzenie panelu z przyciskami do przełączania stron
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

    def dvd_borrow_view(self):
        self.__controller.set_selected_dvd_id(self.__selected_dvd)
        self.__controller.change_view('dvd_borrow')

    def dvd_edit_view(self):
        self.__controller.set_selected_dvd_id(self.__selected_dvd)
        self.__controller.change_view('dvd_edit')

    def __next_page(self):
        print(self.__dvds_count)
        if self.__dvds_count - (self.__page * 10) > 0:
            self.__page += 1
            self.__update_page()

    def __prev_page(self):
        if self.__page > 1:
            self.__page -= 1
            self.__update_page()

    def __update_page(self):
        for label in self.__page_labels:
            label.configure(text = str(self.__page))
        self.__create_search(self.__dvd_frames_container)

