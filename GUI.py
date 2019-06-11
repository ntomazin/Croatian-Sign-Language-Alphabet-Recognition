import tkinter
import os
from threading import Thread


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


        self.start_btn = tkinter.Button(self.f1, text='Prepoznavanje geste', bg='black', fg='white', font=("Calibri", 18),
                                    activebackground='white', activeforeground='black',
                                    command=lambda: (self.prepoznaj()))
        self.start_btn.place(relx=0.5, rely=0.2, anchor="center")

        self.dodaj_btn = tkinter.Button(self.f1, text='Dodaj gestu', bg='black', fg='white',
                                        font=("Calibri", 18),
                                        activebackground='white', activeforeground='black',
                                        command=lambda: (self.dodaj_gestu()))
        self.dodaj_btn.place(relx=0.5, rely=0.4, anchor="center")


        self.treniraj_btn = tkinter.Button(self.f1, text='Treniraj mrežu', bg='black', fg='white',
                                        font=("Calibri", 18),
                                        activebackground='white', activeforeground='black',
                                        command=lambda: (self.treniraj()))
        self.treniraj_btn.place(relx=0.5, rely=0.6, anchor="center")


        # about button
        self.about_btn = tkinter.Button(self.f1, text='Opis', bg='black', fg='white', font=("Calibri", 18),
                                       activebackground='white', activeforeground='black',
                                       command=lambda: (self.about()))
        self.about_btn.place(relx=0.5, rely=0.8, anchor="center")


        self.slika_btn = tkinter.Button(self.f1, text='Geste', bg='black', fg='white', font=("Calibri", 18),
                                        activebackground='white', activeforeground='black',
                                        command=lambda: (Thread(target=self.slika())))
        self.slika_btn.place(relx=0.8, rely=0.8, anchor="center")

        self.izlaz_btn = tkinter.Button(self.f1, text='Izlaz', bg='black', fg='white', font=("Calibri", 18),
                                        activebackground='white', activeforeground='black',
                                        command=lambda: (Thread(target=self.close_window())))
        self.izlaz_btn.place(relx=0.2, rely=0.8, anchor="center")

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

        self.back_btn = tkinter.Button(self.f2, text='Natrag', bg='black', fg='white', font=("Calibri", 18),
                                       activebackground='white', activeforeground='black',
                                       command=lambda: (self.f2.destroy(), self.main_frame()))
        self.back_btn.place(x=280, y=300)

    def prepoznaj(self):
        from recognize import main
        main()
    def dodaj_gestu(self):
        from add_gesture import main
        main()
    def treniraj(self):
        import load_img, model
        load_img.main()
        model.main()
    def slika(self):
        os.system("eog znakovni-jezik-abeceda.jpg")

Settings()

