import tkinter as tk
from tkinter import ttk
from src.database.database_manager import DatabaseManager
from src.views.dvd_search_view import DVDSearchView
from src.frames import HeaderFrame
from src.views import DVDAddView
from src.views import DVDEditView
from src.views import HistoryLogView
from src.views import DVDBorrowView
from src.views import DVDReturnView

class Application(tk.Tk):
    __views = {
        "dvd_search": DVDSearchView,
        "dvd_add": DVDAddView,
        "dvd_edit": DVDEditView,
        "history_log": HistoryLogView,
        "dvd_borrow": DVDBorrowView,
        "dvd_return": DVDReturnView,
    }
    def __init__(self):
        super().__init__()
        self.__selected_dvd_id = -1
        self.__current_view = None
        self.__view_container = None
        self.__current_view_window = None

        DatabaseManager.check_database()
        self.title("DVD Aplication")
        self.geometry("1280x720")
        self.configure(bg='#555')
        self.__create_main_view()

    def get_selected_dvd_id(self):
        return self.__selected_dvd_id

    def set_selected_dvd_id(self, dvd_id):
        self.__selected_dvd_id = dvd_id

    def __create_main_view(self):
        # Header
        header = HeaderFrame(self, self)
        header.pack(fill='both')
        # View Kontener
        self.__view_container = tk.Frame(self)
        self.__view_container.pack(fill='both', expand=True)

        self.__view_canvas = tk.Canvas(self.__view_container, background='#555')
        self.__view_canvas.pack(side='left', fill='both', expand=True)

        scrollbar = tk.Scrollbar(self.__view_container, command=self.__view_canvas.yview)
        scrollbar.pack(side='right', fill='y')

        self.__view_canvas.configure(yscrollcommand=scrollbar.set)
        self.__view_canvas.bind("<Configure>", self.on_configure)
        self.change_view('dvd_search')

    def change_view(self, view:str):
        if self.__current_view is not None:
            self.__view_canvas.delete(self.__current_view_window)
            self.__current_view.destroy()
        self.__current_view = self.__views[view](self.__view_canvas, self)
        self.__current_view_window = self.__view_canvas.create_window(
            (0,0), window=self.__current_view, anchor='nw', width=self.__view_canvas.winfo_width(),
        )

    def on_configure(self, event):
        self.__view_canvas.configure(scrollregion=self.__view_canvas.bbox("all"))
        self.__view_canvas.itemconfig(self.__current_view_window, width=event.width)

