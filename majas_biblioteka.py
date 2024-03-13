import sqlite3
from tkinter import ttk
import tkinter as tk

class MajasBiblioteka:
    def __init__(self, root):
        self.root = root
        self.izveidot_interfeisu()
        savienojums = sqlite3.connect("majas_biblioteka.db")
        kursors = savienojums.cursor()

        kursors.execute(''' CREATE TABLE IF NOT EXISTS "gramatas" (
                            "gramatas_id"	INTEGER NOT NULL,
                            "gramatas_nosaukums"	TEXT NOT NULL,
                            "gramatas_autors"	TEXT NOT NULL,
                            "gramatas_publicesanas_gads"	INTEGER NOT NULL,
                            "gramatas_kategorija"	TEXT NOT NULL,
                            PRIMARY KEY("gramatas_id")
                        ); ''')

        kursors.close()
        savienojums.close()

    def izveidot_interfeisu(self):
        
        style = ttk.Style(root)

        root.tk.call('source', 'forest-dark.tcl')
        ttk.Style().theme_use('forest-dark')
        
        style.configure('Accent.TButton', font=('Calibri', 12), height=1, width=15, padding=5)

        self.l_virsraksts = ttk.Label(self.root, text='Sveicināti Mājas bibliotēkā', font=('Helvetica', 25), foreground='#68CACA')
        
        self.b_pievienot_gramatu = ttk.Button(self.root, text="Pievienot grāmatu", style='Accent.TButton', command=self.b_pievienot)

        self.b_izdzest_gramatu = ttk.Button(self.root, text="Izdzēst grāmatu", style='Accent.TButton', command=self.b_izdzest)

        self.b_apskatit_gramatas = ttk.Button(self.root, text="Apskatīt grāmatas", style='Accent.TButton', command=self.b_apskatit)

        self.l_gramatas_nosaukums = tk.Label(self.root, text='Grāmatas nosaukums:', font=(15), fg="red")
        self.e_gramatas_nosaukums = tk.Entry(self.root)

        self.l_gramatas_autors = tk.Label(self.root, text='Grāmatas autors:', font=(15), fg="red")
        self.e_gramatas_autors = tk.Entry(self.root)

        self.l_gramatas_publicesanas_gads = tk.Label(self.root, text='Grāmatas publicēšanas gads:', font=(15), fg="red")
        self.e_gramatas_publicesanas_gads = tk.Entry(self.root)

        self.l_gramatas_kategorija = tk.Label(self.root, text='Grāmatas kategorija:', font=(15), fg="red")
        self.e_gramatas_kategorija = tk.Entry(self.root)

        self.b_iesniegt = ttk.Button(self.root, text="Iesniegt", style='Accent.TButton', command=self.pievienot_gramatu)
        self.b_atpakal = ttk.Button(self.root, text="Atgriezties", style='Accent.TButton', command=self.b_atgriezties)

        self.l_zinojums = tk.Label(self.root, text='', font=('Calibri', 20, 'bold'), fg="black")
        
        self.tabula = ttk.Treeview(self.root, selectmode ='browse')
        
        self.vertikala_ritjosla = ttk.Scrollbar(self.root, orient="vertical", command=self.tabula.yview)
        
        self.l_meklet = tk.Label(self.root, text='Meklēt:', font=(15), fg="red")
        self.e_meklet = tk.Entry(self.root)

        self.l_meklet_kategorija = tk.Label(self.root, text='Meklēt kategorijā:', font=(15), fg="red")

        self.kategorijas = {
            "Nosaukums": "gramatas_nosaukums",
            "Autors": "gramatas_autors",
            "Kategorija": "gramatas_kategorija",
            "Publicēšanas gads": "gramatas_publicesanas_gads"
        }

        self.c_meklet_kategorija = ttk.Combobox(self.root, values=list(self.kategorijas.keys()), state='readonly')
        self.c_meklet_kategorija.set("Nosaukums")

        self.b_meklet = ttk.Button(self.root, text="Meklēt", style='Accent.TButton', command=self.meklet_gramatas)
        
        self.b_dzest = ttk.Button(self.root, text="Dzēst grāmatu", style='Accent.TButton', command=self.izdzest_gramatu)

        self.l_virsraksts.place(relx=0.5, y=30, anchor='n')
        self.b_pievienot_gramatu.place(relx=0.5, y=130, anchor='n')
        self.b_izdzest_gramatu.place(relx=0.5, y=180, anchor='n')
        self.b_apskatit_gramatas.place(relx=0.5, y=230, anchor='n')
        
    def meklet_gramatas(self):
        if not self.e_meklet.get().lower() or not self.c_meklet_kategorija.get():
            return

        meklesanas_kategorija = self.kategorijas.get(self.c_meklet_kategorija.get(), "")
        if not meklesanas_kategorija:
            return

        savienojums = sqlite3.connect("majas_biblioteka.db")
        kursors = savienojums.cursor()

        kursors.execute(f"SELECT gramatas_nosaukums, gramatas_autors, gramatas_publicesanas_gads, gramatas_kategorija FROM gramatas WHERE lower({meklesanas_kategorija}) LIKE ?",
                        ('%' + self.e_meklet.get().lower() + '%',))

        meklesanas_rezultati = kursors.fetchall()

        for gramata in self.tabula.get_children():
            self.tabula.delete(gramata)

        for gramata in meklesanas_rezultati:
            self.tabula.insert("", 'end', values=gramata)

        kursors.close()
        savienojums.close()

    def pievienot_gramatu(self):
        gramatas_nosaukums = self.e_gramatas_nosaukums.get()
        gramatas_autors = self.e_gramatas_autors.get()
        gramatas_publicesanas_gads = self.e_gramatas_publicesanas_gads.get()
        gramatas_kategorija = self.e_gramatas_kategorija.get()

        if gramatas_nosaukums and gramatas_autors and gramatas_publicesanas_gads and gramatas_kategorija != "":
            savienojums = sqlite3.connect("majas_biblioteka.db")
            kursors = savienojums.cursor()

            kursors.execute(''' INSERT INTO gramatas(gramatas_nosaukums, gramatas_autors, gramatas_publicesanas_gads, gramatas_kategorija)
                VALUES(?,?,?,?) ''', (gramatas_nosaukums, gramatas_autors, gramatas_publicesanas_gads, gramatas_kategorija))

            savienojums.commit()
            savienojums.close()

            self.l_zinojums.config(fg="green", text="Grāmata tika pievienota")
            self.e_gramatas_nosaukums.delete(0, tk.END)
            self.e_gramatas_autors.delete(0, tk.END)
            self.e_gramatas_publicesanas_gads.delete(0, tk.END)
            self.e_gramatas_kategorija.delete(0, tk.END)
        else:
            self.l_zinojums.config(fg="red", text="Jābūt aizpildītiem visiem laukiem")

    def izdzest_gramatu(self):
        izveleta_gramata = self.tabula.selection()
        if not izveleta_gramata:
            self.l_zinojums.config(fg="red", text="Lūdzu, izvēlieties grāmatu, ko dzēst.")
            return

        gramatas_id = self.tabula.item(izveleta_gramata, "text")
        if not gramatas_id:
            return
        
        savienojums = sqlite3.connect("majas_biblioteka.db")
        kursors = savienojums.cursor()

        kursors.execute("DELETE FROM gramatas WHERE gramatas_id=?", (gramatas_id,))
        savienojums.commit()

        kursors.close()
        savienojums.close()
        
        self.tabula.delete(izveleta_gramata)
            
        self.l_zinojums.config(fg="green", text="Grāmata tika veiksmīgi izdzēsta.")

    def b_pievienot(self):
        self.l_virsraksts.place_forget()
        self.b_pievienot_gramatu.place_forget()
        self.b_izdzest_gramatu.place_forget()
        self.b_apskatit_gramatas.place_forget()
        
        self.l_gramatas_nosaukums.place(relx=0.5, y=10, anchor='n')
        self.e_gramatas_nosaukums.place(relx=0.5, y=40, anchor='n')
        self.l_gramatas_autors.place(relx=0.5, y=70, anchor='n')
        self.e_gramatas_autors.place(relx=0.5, y=100, anchor='n')
        self.l_gramatas_publicesanas_gads.place(relx=0.5, y=130, anchor='n')
        self.e_gramatas_publicesanas_gads.place(relx=0.5, y=160, anchor='n')
        self.l_gramatas_kategorija.place(relx=0.5, y=190, anchor='n')
        self.e_gramatas_kategorija.place(relx=0.5, y=220, anchor='n')
        self.b_iesniegt.place(relx=0.5, y=255, anchor='n')
        self.b_atpakal.place(relx=0.5, y=315, anchor='n')
        self.l_zinojums.place(relx=0.5, y=360, anchor='n')
        self.l_zinojums.config(text="")

    def b_izdzest(self):
        self.l_virsraksts.place_forget()
        self.b_pievienot_gramatu.place_forget()
        self.b_izdzest_gramatu.place_forget()
        self.b_apskatit_gramatas.place_forget()
        
        root.geometry("1024x768+" + str((root.winfo_screenwidth() - 1024) // 2) + "+" + str((root.winfo_screenheight() - 768) // 2))
        
        self.l_zinojums.place(relx=0.5, y=600, anchor='n')
        self.l_zinojums.config(text="")
        
        self.tabula.place(relx=0.5, y=300, anchor='center')

        self.vertikala_ritjosla.place(relx=0.92, y=300, anchor='e', relheight=0.7)

        self.tabula.configure(yscrollcommand=self.vertikala_ritjosla.set)

        self.tabula["columns"] = ("1", "2", "3", "4")

        self.tabula['show'] = 'headings'

        self.tabula.column("1", width = 200, anchor ='w')
        self.tabula.column("2", width = 200, anchor ='w')
        self.tabula.column("3", width = 200, anchor ='w')
        self.tabula.column("4", width = 200, anchor ='w')

        self.tabula.heading("1", text ="Nosaukums")
        self.tabula.heading("2", text ="Autors")
        self.tabula.heading("3", text ="Publicēšanas gads")
        self.tabula.heading("4", text ="Kategorija")
        
        self.tabula["height"] = 25 
        
        savienojums = sqlite3.connect("majas_biblioteka.db")
        kursors = savienojums.cursor()

        kursors.execute("SELECT * FROM gramatas")
        gramatas = kursors.fetchall()
        
        for gramata in gramatas:
            self.tabula.insert("", 'end', text=gramata[0], values=gramata[1:])

        kursors.close()
        savienojums.close()
        
        self.b_dzest.place(relx=0.5, y=645, anchor='n')
        
        self.b_atpakal.place(relx=0.5, y=700, anchor='n')

    def b_apskatit(self):
        self.l_virsraksts.place_forget()
        self.b_pievienot_gramatu.place_forget()
        self.b_izdzest_gramatu.place_forget()
        self.b_apskatit_gramatas.place_forget()
        
        root.geometry("1024x768+" + str((root.winfo_screenwidth() - 1024) // 2) + "+" + str((root.winfo_screenheight() - 768) // 2))
        
        self.tabula.place(relx=0.5, y=300, anchor='center')

        self.vertikala_ritjosla.place(relx=0.92, y=300, anchor='e', relheight=0.7)

        self.tabula.configure(yscrollcommand=self.vertikala_ritjosla.set)

        self.tabula["columns"] = ("1", "2", "3", "4")

        self.tabula['show'] = 'headings'

        self.tabula.column("1", width = 200, anchor ='w')
        self.tabula.column("2", width = 200, anchor ='w')
        self.tabula.column("3", width = 200, anchor ='w')
        self.tabula.column("4", width = 200, anchor ='w')

        self.tabula.heading("1", text ="Nosaukums")
        self.tabula.heading("2", text ="Autors")
        self.tabula.heading("3", text ="Publicēšanas gads")
        self.tabula.heading("4", text ="Kategorija")
        
        self.tabula["height"] = 25 
        
        savienojums = sqlite3.connect("majas_biblioteka.db")
        kursors = savienojums.cursor()

        kursors.execute("SELECT * FROM gramatas")
        gramatas = kursors.fetchall()
        
        for gramata in gramatas:
            self.tabula.insert("", 'end', text=gramata[0], values=gramata[1:])

        kursors.close()
        savienojums.close()
        
        self.l_meklet.place(relx=0.5, y=580, anchor='n')

        self.e_meklet.place(relx=0.5, y=605, anchor='n')

        self.l_meklet_kategorija.place(relx=0.5, y=630, anchor='n')

        self.c_meklet_kategorija.place(relx=0.5, y=660, anchor='n')
        
        self.b_meklet.place(relx=0.4, y=710, anchor='n')
        
        self.b_atpakal.place(relx=0.6, y=710, anchor='n')
        

    def b_atgriezties(self):
        for gramata in self.tabula.get_children():
            self.tabula.delete(gramata)
            
        self.e_gramatas_nosaukums.delete(0, tk.END)
        self.e_gramatas_autors.delete(0, tk.END)
        self.e_gramatas_publicesanas_gads.delete(0, tk.END)
        self.e_gramatas_kategorija.delete(0, tk.END)
        
        self.l_gramatas_nosaukums.place_forget()
        self.e_gramatas_nosaukums.place_forget()
        self.l_gramatas_autors.place_forget()
        self.e_gramatas_autors.place_forget()
        self.l_gramatas_publicesanas_gads.place_forget()
        self.e_gramatas_publicesanas_gads.place_forget()
        self.l_gramatas_kategorija.place_forget()
        self.e_gramatas_kategorija.place_forget()
        self.b_iesniegt.place_forget()
        self.b_atpakal.place_forget()
        self.l_zinojums.place_forget()
        self.tabula.place_forget()
        self.vertikala_ritjosla.place_forget()
        self.l_meklet.place_forget()
        self.e_meklet.place_forget()
        self.l_meklet_kategorija.place_forget()
        self.c_meklet_kategorija.place_forget()
        self.b_meklet.place_forget()
        self.b_dzest.place_forget()
        
        root.geometry("500x400+" + str((root.winfo_screenwidth() - 400) // 2) + "+" + str((root.winfo_screenheight() - 500) // 2))
        
        self.l_virsraksts.place(relx=0.5, y=30, anchor='n')
        self.b_pievienot_gramatu.place(relx=0.5, y=130, anchor='n')
        self.b_izdzest_gramatu.place(relx=0.5, y=180, anchor='n')
        self.b_apskatit_gramatas.place(relx=0.5, y=230, anchor='n')
        
root = tk.Tk()
root.title("Mājas bibliotēka")
root.geometry("500x400+" + str((root.winfo_screenwidth() - 400) // 2) + "+" + str((root.winfo_screenheight() - 500) // 2))
root.resizable(0, 0)

MajasBiblioteka(root)

root.mainloop()
