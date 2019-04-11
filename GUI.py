import tkinter


class Settings:

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.geometry("640x420")
        self.root.resizable(False, False)
        self.root.title('Prepoznavanje hrvatske znakovne abecede')
        super().__init__()
        self.main_frame()
        self.root.mainloop()

    def main_frame(self):
        self.f1 = tkinter.Frame(self.root, width=640, height=420, bg='white')
        self.f1.pack(fill=tkinter.X)

        Uvod =   'Nakon pritiska na gumb pokreni\n' \
                 'potretno je označiti pravokutnik\n' \
                 'koji će prestavljati područje gdje će se prvo\n'\
                 'iščitati histogram koze te nakon\n'\
                 'će koristiti kao mjesto za pokazivanje slova.\n'
        main_label = tkinter.Label(self.f1, text=Uvod, font=("Calibri", 15), fg='black', bg='white')
        main_label.place(x=90, y=0)

        self.start_btn = tkinter.Button(self.f1, text='Početak', bg='black', fg='white', font=("Calibri", 18),
                                    activebackground='white', activeforeground='black',
                                    command=lambda: (self.close_window()))
        self.start_btn.place(x=10, y=350)


        # about button
        self.about_btn = tkinter.Button(self.f1, text='Opis', bg='black', fg='white', font=("Calibri", 18),
                                       activebackground='white', activeforeground='black',
                                       command=lambda: (self.about()))
        self.about_btn.place(x=200, y=350)

    def close_window(self):
        self.root.destroy()

    def about(self):
        self.f1.destroy()
        self.f2 = tkinter.Frame(self.root, width=500, height=420, bg='white')
        self.f2.pack(fill=tkinter.X)

        result = 'Autor: Nikola Tomažin\nOpis:\n' \
                 'Ovo je projekt koji radim za završni rad\nna fakultetu elektrotehnike i računarstva(FER).\n' \
                 'tema je prepoznavanje hrvatkog znakovnog\n jezika.'
        last = tkinter.Label(self.f2, text=result, font=("Calibri", 15), fg='black', bg='white')
        last.place(x=90, y=0)

        self.back_btn = tkinter.Button(self.f2, text='Back', bg='black', fg='white', font=("Calibri", 18),
                                       activebackground='white', activeforeground='black',
                                       command=lambda: (self.f2.destroy(), self.main_frame()))
        self.back_btn.place(x=280, y=300)

