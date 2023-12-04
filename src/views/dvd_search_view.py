from tkinter import ttk
import tkinter as tk

class DVDSearchView(ttk.Frame):
    def __init__(self, parent, controler):
        super().__init__(parent, width=parent.winfo_reqwidth())
        self.configure(style="ViewBG.TFrame")

        self.dvd_frames = []
        self.search_bar = self.create_search_bar()
        self.create_button_bar()
        self.dvd_frames_container = ttk.Frame(self)
        self.dvd_frames_container.pack(fill='x', padx=50)
        self.create_search()
        self.create_button_bar()
    
    def create_search_bar(self):
        sb = ttk.Frame(self)
        sb.pack(pady=10)
        entry = ttk.Entry(sb, width=40)
        entry.pack(side='left')
        submit = ttk.Button(sb, text="Submit", command=self.on_submit)
        submit.pack(side='left', padx=10)
        return sb

    def on_submit(self):
        print("click :smile:")

    def create_search(self):
        for dvd_frame in self.dvd_frames:
            dvd_frame.destroy()
        self.dvd_frames = []
        for i in range(10):
            dvd = self.create_dvd_frame()
            self.dvd_frames.append(dvd)


    def create_dvd_frame(self):
        dvd_frame = tk.Frame(self.dvd_frames_container, borderwidth=3, relief='solid')
        dvd_frame.pack(anchor='w', pady=15, padx=10)
        ttk.Label(dvd_frame, text="Tytuł filmu").pack(anchor='w')
        ttk.Label(dvd_frame, text="Opis filmu").pack(anchor='w')
        ttk.Label(dvd_frame, text="Rok wydania").pack(anchor='w')
        cat_frame = ttk.Frame(dvd_frame)
        cat_frame.pack(anchor='w')
        for i in range(4):
            lab = ttk.Label(cat_frame, text="Category")
            lab.pack(padx=10, side='left')
        ttk.Label(dvd_frame, text="liczba kopii: 2").pack(anchor='w')
        return dvd_frame

    def create_button_bar(self):
        bottom_bar = ttk.Frame(self)
        left_button = ttk.Button(bottom_bar, text="<")
        left_button.pack(side='left')
        ttk.Label(bottom_bar, text="1").pack(padx=30, side='left')
        right_button = ttk.Button(bottom_bar, text=">")
        right_button.pack(side='left')
        bottom_bar.pack(pady=10)

