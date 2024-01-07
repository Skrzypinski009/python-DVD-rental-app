from tkinter import ttk 

class DVDBorrowView(ttk.Frame):
     def __init__(self, parent, controler, selected_dvd=-1):
        super().__init__(parent, width=parent.winfo_reqwidth())
        self.selected_dvd = selected_dvd

        container = ttk.Frame(self)

        container.pack(fill='x', expand=True, padx=(50,0), pady=(50,0))
        ttk.Label(container, text="Wyporzyczanie pozycji", font=('Arial', 22)).pack(pady=20, padx=20)

        ttk.Label(container, text='Dane Klijenta', font=('Arial', 18)).pack(anchor='w',pady=20, padx=20)
        ttk.Label(container, text='Imie: ', font=('Arial',14)).pack(anchor='w',padx=50)
        ttk.Entry(container, width=40).pack(anchor='w', padx=70)    
        ttk.Label(container, text='Nazwisko: ', font=('Arial',14)).pack(anchor='w', padx=50)
        ttk.Entry(container, width=40).pack(anchor='w', padx=70)    
        ttk.Label(container, text='E-mail: ', font=('Arial',14)).pack(anchor='w', padx=50)
        ttk.Entry(container, width=40).pack(anchor='w', padx=70)    
       

        ttk.Label(container, text='Dane DVD', font=('Arial', 18)).pack(anchor='w',pady=20, padx=20)
        ttk.Label(container, text='Nazwa: ', font=('Arial',14)).pack(anchor='w', padx=50)
        ttk.Entry(container, width=40).pack(anchor='w', padx=70)    
        ttk.Label(container, text='Kod kopi: ', font=('Arial',14)).pack(anchor='w', padx=50)
        ttk.Entry(container, width=40).pack(anchor='w', padx=70)   
      
       
        ttk.Button(container, text='Submit').pack(anchor='w', padx=10, pady=25) 

        label = ttk.Label(self, text="DVDBorrowView")
        label.pack()
