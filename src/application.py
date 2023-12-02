import tkinter as tk
from tkinter import ttk
from src.views.dvd_search_view import DVDSearchView
from src.frames.header_frame import HeaderFrame

class Application(tk.Tk):
    views = {
        "dvd_search": DVDSearchView,
    }
    def __init__(self):
        super().__init__();
        self.title("Ale jaja")
        self.geometry("800x600")
        self.configure_styles()
        self.create_main_view()
        self.change_view("dvd_search")

    def create_main_view(self):
        self.current_view = None
        header = HeaderFrame(self, self)
        header.pack(side="top", fill='both')
        header.configure(style='Header.TFrame')
        self.view_container = tk.ttk.Frame(self).pack(fill='y')
        
    def change_view(self, view:str):
        if self.current_view is not None:
            self.current_view.destroy()
        self.current_view = self.views[view](self.view_container, self)

    def configure_styles(self):
        self.style = ttk.Style()
        #self.style.theme_use('clam')
        self.style.configure('Header.TFrame', background='#333', relief='flat') 
        self.style.configure(
            'Header.TButton', 
            background='#222', 
            foreground='#ddd', 
            relief='flat', 
            width=10, 
            font=('Arial', 16, 'normal')
        )
