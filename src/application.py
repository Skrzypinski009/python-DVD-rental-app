import tkinter as tk
from tkinter import ttk
from src.views.dvd_search_view import DVDSearchView
from src.frames.header_frame import HeaderFrame
from src.views.dvd_add_view import DVDAddView
from src.views.dvd_edit_view import DVDEditView
from src.views.history_log_view import HistoryLogView
from src.views.dvd_borrow_view import DVDBorrowView

class Application(tk.Tk):
    views = {
        "dvd_search": DVDSearchView,
        "dvd_add": DVDAddView,
        "dvd_edit": DVDEditView,
        "history_log": HistoryLogView,
        "dvd_borrow": DVDBorrowView,
    }
    def __init__(self):
        super().__init__()
        self.title("Ale jaja")
        self.geometry("800x600")
        self.configure_styles()
        self.create_main_view()

    def create_main_view(self):
        self.current_view = None
        header = HeaderFrame(self, self)
        header.pack(side="top", fill='both')
        header.configure(style='Header.TFrame')
        self.view_container = tk.ttk.Frame(self)
        self.view_container.configure(style="ViewContainer.TFrame")
        self.view_container.pack(fill='both', expand=True)
        self.view_canvas = tk.Canvas(self.view_container)
        self.view_canvas.pack(side='left', fill='both', expand=True)
        scrollbar = tk.ttk.Scrollbar(self.view_container, command=self.view_canvas.yview)
        scrollbar.pack(side='right', fill='y')
        self.view_canvas.configure(yscrollcommand=scrollbar.set)
        self.view_canvas.bind("<Configure>", self.on_configure)
        self.change_view('dvd_borrow')

    def change_view(self, view:str):
        if self.current_view is not None:
            self.view_canvas.delete(self.current_view_window)
            self.current_view.destroy()
        self.current_view = self.views[view](self.view_canvas, self)
        self.current_view_window = self.view_canvas.create_window((0,0), window=self.current_view, anchor='nw')


    def configure_styles(self):
        self.style = ttk.Style()
        #self.style.theme_use('clam')
        # self.style.configure('View.TLabel', background='red')
        # self.style.configure('View.TFrame', background='blue')
        self.style.configure('Header.TFrame', background='#333', relief='flat') 
        self.style.configure(
            'Header.TButton', 
            background='#222', 
            foreground='#ddd', 
            relief='flat', 
            font=('Arial', 16, 'normal')
        )

    def on_configure(self, event):
        self.view_canvas.configure(scrollregion=self.view_canvas.bbox("all"))
        self.view_canvas.itemconfig(self.current_view_window, width=event.width)

