import tkinter as tk

class HeaderFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, background='#333')
        self.__bg_color = '#333'
        self.__controller = controller

        self.__padding_frame = tk.Frame(self, bg='#333')
        self.__padding_frame.pack(padx=5, pady=8, fill='both')

        self.__create_button('DVD Search', self.__dvd_search_view)
        self.__create_button('DVD Add', self.__dvd_add_view)
        self.__create_button('Return DVD', self.__dvd_return_view)
        self.__create_button('Rental History', self.__history_log_view)
        
    def __create_button(self, text, command):
        button = tk.Button(
            self.__padding_frame, text=text, width=14, command=command,
            bg='#222', fg='white',
            activebackground='#444', activeforeground='white',
            font=('Arial', 16), relief='flat'
        )
        button.pack(side='left', padx=15)
    
    def __dvd_search_view(self):
        self.__controller.change_view('dvd_search')

    def __dvd_add_view(self):
        self.__controller.change_view('dvd_add')

    def __dvd_return_view(self):
        self.__controller.change_view('dvd_return')

    def __history_log_view(self):
        self.__controller.change_view('history_log')

