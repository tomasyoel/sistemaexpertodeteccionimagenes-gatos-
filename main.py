from ctypes import sizeof
#from lib2to3.pgen2.token import LEFTSHIFT
from logging import RootLogger
from operator import length_hint
from select import select
from tkinter import *
from tkinter import filedialog as fd
import shutil
import copy
import os
import tkinter
from turtle import width
from PIL import ImageTk,Image
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import threading
import os
import random
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class graph_frame(Frame):
    def __init__(self):
        Frame.__init__(self,root)
    
    def add_graph(self,fig):
        self.mpl_canvas=FigureCanvasTkAgg(fig,self)
        
        self.mpl_canvas.get_tk_widget().pack(fill=BOTH,expand=True)
        self.mpl_canvas._tkcanvas.pack( fill=BOTH, expand=True)
    def remove_graph(self):
        self.mpl_canvas.get_tk_widget().pack_forget()
        self.mpl_canvas._tkcanvas.pack_forget()
        del self.mpl_canvas

class cat:
    def __init__(self)->None:
        self.name =""
        self.description=""
        self.temperament=""
        self.origin=""
        self.comments=""
        self.image="sources/default.jpeg"

        # caracteristics
        self.caracteristics={}

class visualizer:
    def __init__(self,menu,frame1,cat,rules,clasifier)->None:
        self.frame1=frame1
        self.clasifier=clasifier
        self.name=Label(self.frame1, text="RAZA DE GATO", background='#353437')
        self.name.configure(font=("Arial", 50))

        openImage=Image.open(cat.image)
        img=openImage.resize((200, 300))
        self.photo=ImageTk.PhotoImage(img)
        self.image=Label(self.frame1, image=self.photo)

        self.description=Label(self.frame1, text="DESCRIPCIÓN", background='#353437')
        self.description.configure(font=("Arial", 40))
        self.temperament=Label(self.frame1, text="TEMPERAMENTO", background='#353437')
        self.temperament.configure(font=("Arial", 40))
        self.origin=Label(self.frame1, text="ORIGEN", background='#353437')
        self.origin.configure(font=("Arial", 40))
        self.comments=Label(self.frame1, text="COMENTARIOS", background='#353437')
        self.comments.configure(font=("Arial", 40))
        self.explanation=Label(self.frame1, text="EXPLICACIÓN", background='#353437')
        self.explanation.configure(font=("Arial", 40))
        self.menu_window=menu
        self.cat=cat
        self.rules=rules
        self.addButton=Button(self.frame1, text="Agregar Raza", command=self.add_cat, bg="#7a7b7c", fg="white")
        self.addButton.config(height=2, width=15)
        self.menuButton=Button(self.frame1, text="Menú Principal", command=self.main_window, bg="#7a7b7c", fg="white")
        self.menuButton.config(height=2, width=15)
        self.showCat()

    def add_cat(self):
        self.addfunction=addCat(self.menu_window,self.frame1,self.clasifier)
        self.hide()
        self.addfunction.show()

    def show(self):
        self.name.pack()
        self.image.pack()
        self.description.pack()
        self.temperament.pack()
        self.origin.pack()
        self.comments.pack()
        self.explanation.pack()

        if(self.cat.name=="Desconocida"):
            self.addButton.pack(side=TOP)
        self.menuButton.pack(side=TOP)

    # Oculta la vista de la descripción del gato
    def hide(self):
        self.name.pack_forget()
        self.image.pack_forget()
        self.description.pack_forget()
        self.temperament.pack_forget()
        self.origin.pack_forget()
        self.comments.pack_forget()
        self.explanation.pack_forget()
        if(self.cat.name == "Desconocida"):
            self.addButton.pack_forget()
        self.menuButton.pack_forget()

    def showCat(self):
        self.name=Label(self.frame1,text=self.cat.name, background='#353437', fg="white")
        self.name.configure(font=("Arial", 35))

        openImage=Image.open(self.cat.image)
        img = openImage.resize((200, 200))
        self.photo=ImageTk.PhotoImage(img)
        self.image=Label(self.frame1, image=self.photo)

        self.description=Label(self.frame1,text=self.cat.description, wraplength=1200, background='#353437', fg="white")
        self.description.configure(font=("Arial", 14))
        self.temperament=Label(self.frame1,text=self.cat.temperament, wraplength=1200, background='#353437', fg="white")
        self.temperament.configure(font=("Arial", 14))
        self.origin=Label(self.frame1,text=self.cat.origin, wraplength=1200, background='#353437', fg="white")
        self.origin.configure(font=("Arial", 14))
        self.comments=Label(self.frame1,text=self.cat.comments, wraplength=1200, background='#353437', fg="white")
        self.comments.configure(font=("Arial", 14))
        exp="\n\n\nLa raza fue encontrada en base a las siguientes características:\n"
        for key in self.rules.keys():
            exp+=key+":"+self.rules[key]+"\n"

        self.explanation = Label(self.frame1, text=exp, wraplength=1200, background='#353437', fg="white")
        self.explanation.configure(font=("Arial", 14))

    # Muestra la vista principal
    def main_window(self):
        self.hide()
        self.menu_window.show()

    def closing(self):
        del self

class addCat:
    def __init__(self, menu, frame1, clasifier) -> None:
        self.frame1 = frame1
        self.main_menu = menu
        self.clasifier = clasifier
        self.load_caracteristics()
        self.labels = []
        self.entries = []

        for caracteristic in self.caracteristics:
            self.labels.append(Label(self.frame1, text=caracteristic.capitalize(), background='#353437', fg="white"))
            if(caracteristic == "descripcion" or caracteristic == "temperamento" or caracteristic == "comentarios"):
                self.entries.append(Text(self.frame1, height=2, width=45))
            else:
                self.entries.append(Entry(self.frame1, width=60))

    def load_caracteristics(self):
        self.caracteristics = []
        self.caracteristics.append("nombre")
        self.caracteristics.append("descripcion")
        self.caracteristics.append("temperamento")
        self.caracteristics.append("comentarios")
        self.caracteristics.append("color")
        self.caracteristics.append("pelo")
        self.caracteristics.append("tamaño")
        self.caracteristics.append("origen")

    def show(self):
        self.title=Label(self.frame1, text="Agregar Raza de Gato", background='#353437', fg="white")
        self.title.configure(font=("Arial", 20))
        self.title.grid(column=1,row=1,columnspan=5)
        self.currentpos=3
        for i in range(len(self.labels)):
            self.labels[i].configure(font=("Arial", 15))
            self.labels[i].grid(column=1,row=self.currentpos)
            self.entries[i].grid(column=2,row=self.currentpos)
            if(self.caracteristics[i]=="comentarios"):
                self.currentpos+=1
                self.instructions=Label(self.frame1, text="Indique las características de la raza de gato", background='#353437', fg="white")
                self.instructions.configure(font=("Arial", 20))
                self.instructions.grid(column=1, row=self.currentpos, columnspan=2)
            self.currentpos+=1

        self.filename = StringVar()
        self.image = Label(self.frame1, text="Imagen", background='#353437', fg="white")
        self.image.configure(font=("Arial", 15))
        self.image.grid(column=1, row=23)
        self.showRute = Entry(self.frame1, textvariable=self.filename)
        self.showRute.config(state='disabled', width=60)
        self.showRute.grid(column=2, row=23)
        self.chooseImage = Button(self.frame1, text="Seleccionar Imagen", command=self.selectImage, bg="#7a7b7c", fg="white")
        self.chooseImage.config(height=1, width=15)
        self.chooseImage.grid(column=3, row=23)
        self.saveButton = Button(self.frame1, text="Guardar", command=self.save, bg="#7a7b7c", fg="white")
        self.saveButton.config(height=2, width=15)
        self.saveButton.grid(column=2, row=27)
        self.menuButton = Button(self.frame1, text="Menú Principal", command=self.main_window, bg="#7a7b7c", fg="white")
        self.menuButton.config(height=2, width=15)
        self.menuButton.grid(column=1, row=27)
    
    def selectImage(self):
        self.filename.set(fd.askopenfilename(initialdir="/",title="Seleccionar imagen",filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*"))))

    def hide(self):
        self.title.grid_remove()
        for i in range(len(self.labels)):
            self.labels[i].grid_remove()
            self.entries[i].grid_remove()
        self.chooseImage.grid_remove()
        self.instructions.grid_remove()
        self.image.grid_remove()
        self.showRute.grid_remove()
        self.saveButton.grid_remove()
        self.menuButton.grid_remove()

    def save(self):
        self.aux = cat()
        for i in range(len(self.entries)):
            if(self.caracteristics[i] == "descripcion" or self.caracteristics[i] == "temperamento" or self.caracteristics[i] == "comentarios"):
                if(self.caracteristics[i] == "descripcion"):
                    self.aux.description = self.entries[i].get(1.0, "end-1c")
                elif(self.caracteristics[i] == "temperamento"):
                    self.aux.temperament = self.entries[i].get(1.0, "end-1c")
                elif(self.caracteristics[i] == "comentarios"):
                    self.aux.comments = self.entries[i].get(1.0, "end-1c")
            else:
                if(self.entries[i].get() != ""):
                    if(self.caracteristics[i] == "nombre"):
                        self.aux.name = self.entries[i].get()
                    else:
                        self.aux.caracteristics[self.caracteristics[i]] = self.entries[i].get()
        self.currentpath=os.getcwd()
        self.currentpath+="\\sources\\"
        shutil.copy(self.filename.get(), self.currentpath)
        self.words = self.filename.get().split("/")
        self.aux.image = "sources/" + self.words[-1]
        self.clasifier.cats.append(self.aux)
        self.hide()
        self.main_menu.show()

    def main_window(self):
        self.hide()
        self.main_menu.show()

class clasifier:
# Constructor de la clase
    def __init__(self,menu,frame1) -> None:
        self.menu_window=menu
        self.frame1=frame1
        self.title=Label(self.frame1, text="Clasificador de razas de gatos", background='#353437', fg="white")
        self.title.configure(font=("Arial", 35))
        self.menuButton=Button(self.frame1, text="Menú Principal", command=self.main_window, bg="#7a7b7c", fg="white")
        self.menuButton.config(height=10, width=50)
        self.cats=[]
        self.default_cat=cat()
        self.load_cats()
        self.loadall()

    def loadall(self):
        self.good=False
        self.doing=True

        self.rules = {}
        self.decition = self.cats[0]
        self.visual = visualizer(self.menu_window,self.frame1,self.decition,self.rules,self)
        self.possible_rules={}
        self.possible_cats=[]

    def load_cats(self):
        self.default_cat.name="Desconocida"
        self.default_cat.image="sources/default.jpeg"

        self.aux=cat()
        self.aux.name="Gato Siamés"
        self.aux.description="El gato siamés es una raza de gato originaria de Tailandia. Son conocidos por su cuerpo delgado y elegante, patas largas y finas, y cabeza triangular con orejas grandes y puntiagudas."
        self.aux.temperament="Los gatos siameses son conocidos por ser enérgicos, inteligentes y muy apegados a sus dueños. Son ruidosos y disfrutan de la compañía humana."
        self.aux.origin="Tailandia"
        self.aux.comments="Los gatos siameses son una de las razas de gatos más antiguas y populares. Su color característico es el sello o 'point', con un cuerpo pálido y puntas más oscuras en las orejas, cola, patas y cara."
        self.aux.caracteristics["color"]="sello"
        self.aux.caracteristics["pelo"]="corto"
        self.aux.caracteristics["tamaño"]="mediano"
        self.aux.image="sources/gato_siames.jpg"
        self.cats.append(self.aux)

        self.aux = cat()
        self.aux.name = "Gato Persa"
        self.aux.description = "El gato persa es una raza de gato de origen antiguo, conocido por su abundante pelo largo y su cara aplastada."
        self.aux.temperament = "Los gatos persas son tranquilos, cariñosos y adaptables. Disfrutan de la compañía humana y son excelentes compañeros."
        self.aux.origin = "Irán"
        self.aux.comments = "Los gatos persas requieren un cepillado regular para evitar que su pelo se enrede. Son una raza popular y adorable."
        self.aux.caracteristics["color"] = "variado"
        self.aux.caracteristics["pelo"] = "largo"
        self.aux.caracteristics["tamaño"] = "mediano"
        self.aux.image = "sources/gato_persa.jpg"
        self.cats.append(self.aux)

        self.aux = cat()
        self.aux.name = "Gato Bengalí"
        self.aux.description = "El gato bengalí es una raza híbrida creada cruzando gatos domésticos con gatos leopardos asiáticos."
        self.aux.temperament = "Los gatos bengalíes son enérgicos, inteligentes y muy activos. Necesitan mucho ejercicio y atención."
        self.aux.origin = "Estados Unidos"
        self.aux.comments = "Los gatos bengalíes tienen un patrón de pelaje similar al de un leopardo, con manchas y rosetas."
        self.aux.caracteristics["color"] = "manchado"
        self.aux.caracteristics["pelo"] = "corto"
        self.aux.caracteristics["tamaño"] = "grande"
        self.aux.image = "sources/gato_bengali.jpg"
        self.cats.append(self.aux)

        self.aux = cat()
        self.aux.name = "Gato Británico de Pelo Corto"
        self.aux.description = "El Británico de Pelo Corto es una raza antigua y robusta, con un cuerpo compacto y musculoso."
        self.aux.temperament = "Son gatos tranquilos, leales y cariñosos con sus dueños. Tienen un temperamento equilibrado y paciente."
        self.aux.origin = "Reino Unido"
        self.aux.comments = "Su pelo corto y denso requiere poco mantenimiento. Son excelentes compañeros y se adaptan bien a la vida en interior."
        self.aux.caracteristics["color"] = "variado"
        self.aux.caracteristics["pelo"] = "corto"
        self.aux.caracteristics["tamaño"] = "mediano"
        self.aux.image = "sources/gato_britanico_pelo_corto.jpg"
        self.cats.append(self.aux)

        self.aux = cat()
        self.aux.name = "Gato Maine Coon"
        self.aux.description = "El Maine Coon es una raza grande y musculosa, conocida por su pelo largo y abundante."
        self.aux.temperament = "Son gatos amigables, inteligentes y adaptables. Disfrutan de la compañía humana y son excelentes cazadores."
        self.aux.origin = "Estados Unidos"
        self.aux.comments = "Es una de las razas de gato más grandes y robustas. Su pelaje requiere cepillado regular para mantenerlo en buenas condiciones."
        self.aux.caracteristics["color"] = "variado"
        self.aux.caracteristics["pelo"] = "largo"
        self.aux.caracteristics["tamaño"] = "grande"
        self.aux.image = "sources/gato_maine_coon.jpg"
        self.cats.append(self.aux)

        self.aux = cat()
        self.aux.name = "Gato Sphynx"
        self.aux.description = "El Sphynx es una raza de gato sin pelo, con una apariencia suave y musculosa."
        self.aux.temperament = "Son gatos cariñosos, juguetones y muy apegados a sus dueños. Disfrutan de la compañía humana y son muy sociables."
        self.aux.origin = "Canadá"
        self.aux.comments = "A pesar de su apariencia sin pelo, los Sphynx requieren ciertos cuidados especiales para mantener su piel sana."
        self.aux.caracteristics["color"] = "variado"
        self.aux.caracteristics["pelo"] = "sin pelo"
        self.aux.caracteristics["tamaño"] = "mediano"
        self.aux.image = "sources/gato_sphynx.jpg"
        self.cats.append(self.aux)

        self.aux = cat()
        self.aux.name = "Gato Ragdoll"
        self.aux.description = "El Ragdoll es una raza de gato semi-longihair conocida por su tamaño grande y su temperamento cariñoso y relajado."
        self.aux.temperament = "Son gatos tranquilos, afectuosos y leales con sus dueños. Se caracterizan por su comportamiento dócil y relajado."
        self.aux.origin = "Estados Unidos"
        self.aux.comments = "Su pelo semi-largo requiere cepillado regular para mantenerlo en buen estado. Son excelentes gatos para familias."
        self.aux.caracteristics["color"] = "variado"
        self.aux.caracteristics["pelo"] = "semi-largo"
        self.aux.caracteristics["tamaño"] = "grande"
        self.aux.image = "sources/gato_ragdoll.jpg"
        self.cats.append(self.aux)

        self.aux = cat()
        self.aux.name = "Gato Birmano"
        self.aux.description = "El Birmano es una raza de gato de origen antiguo, conocido por su pelo corto y sedoso y su cuerpo musculoso."
        self.aux.temperament = "Son gatos cariñosos, inteligentes y leales con sus dueños. Disfrutan de la compañía humana y son excelentes compañeros."
        self.aux.origin = "Birmania (Myanmar)"
        self.aux.comments = "Su pelo corto y brillante requiere poco mantenimiento. Son gatos elegantes y de porte distinguido."
        self.aux.caracteristics["color"] = "sello"
        self.aux.caracteristics["pelo"] = "corto"
        self.aux.caracteristics["tamaño"] = "mediano"
        self.aux.image = "sources/gato_birmano.png"
        self.cats.append(self.aux)

        self.aux = cat()
        self.aux.name = "Gato Abisinio"
        self.aux.description = "El Abisinio es una antigua raza de gato conocida por su pelaje corto y su elegante apariencia."
        self.aux.temperament = "Son gatos activos, inteligentes y curiosos. Disfrutan de la compañía humana y son excelentes compañeros de juego."
        self.aux.origin = "Etiopía"
        self.aux.comments = "Su pelo corto y sedoso es fácil de mantener. Son gatos ágiles y atléticos, con una apariencia muy distintiva."
        self.aux.caracteristics["color"] = "abisingio"
        self.aux.caracteristics["pelo"] = "corto"
        self.aux.caracteristics["tamaño"] = "mediano"
        self.aux.image = "sources/gato_abisinio.jpg"
        self.cats.append(self.aux)

        self.aux = cat()
        self.aux.name = "Gato Exotic Shorthair"
        self.aux.description = "El Exotic Shorthair es una raza de gato de pelo corto y cara aplastada, derivada del Persa."
        self.aux.temperament = "Son gatos tranquilos, cariñosos y adaptables. Disfrutan de la compañía humana y son excelentes compañeros de hogar."
        self.aux.origin = "Estados Unidos"
        self.aux.comments = "Su pelo corto y denso requiere poco mantenimiento. Son gatos adorables y de aspecto característico."
        self.aux.caracteristics["color"] = "variado"
        self.aux.caracteristics["pelo"] = "corto"
        self.aux.caracteristics["tamaño"] = "mediano"
        self.aux.image = "sources/gato_exotic_shorthair.jpg"
        self.cats.append(self.aux)

    def question(self,q,opt):
        options=[]
        options.append("Otro")
        for key in opt.keys():
            options.append(key)
        self.selection=StringVar()
        self.chooses=StringVar()
        self.chooses.set("Otro")
        self.instructions=Label(self.frame1, text="Seleccione la característica de la siguiente parte del gato:\n\n", background='#353437', fg="white")
        self.instructions.configure(font=("Arial", 25))
        self.instructions.pack()
        self.caracteristica = Label(self.frame1, text=q, background='#353437', fg="white")
        self.caracteristica.configure(font=("Arial", 25))
        self.caracteristica.pack()
        self.drop=OptionMenu(self.frame1,self.chooses,*options)
        self.drop.config(height=1, width=20)
        self.drop.pack()
        self.button=Button(self.frame1, text="Siguiente",command=self.clicked,bg="#7a7b7c",fg="white")
        self.button.config(height=2, width=10)
        self.button.pack()
        self.button.wait_variable(self.selection)
        self.cont=0
        self.listo=False
        self.instructions.pack_forget()
        self.drop.pack_forget()
        self.button.pack_forget()
        self.caracteristica.pack_forget()
        return self.selection

    def clicked(self):
        print(self.chooses.get())
        self.selection.set(self.chooses.get())

    def clasify(self):
        self.loadall()
        self.possible_cats = copy.copy(self.cats)
        self.possible_rules = {}
        self.rules = {}
        other = True
        while (other):
            self.possible_rules = {}
            for cat in self.possible_cats:
                for key in cat.caracteristics.keys():
                    if(key not in self.rules):
                        if(key not in self.possible_rules):
                            self.possible_rules[key] = {}
                        if(cat.caracteristics[key] not in self.possible_rules[key]):
                            self.possible_rules[key][cat.caracteristics[key]] = 1
                        else:
                            self.possible_rules[key][cat.caracteristics[key]] += 1

            color = StringVar()
            caracteristic = ""
            for key in self.possible_rules.keys():
                color.set(self.question(key, self.possible_rules[key]).get())
                caracteristic = key
                self.rules[key] = color.get()
                print(color.get())
                break
            index = 0
            elements = len(self.possible_cats)
            while index < elements:
                print(self.possible_cats[index].name)
                if(caracteristic not in self.possible_cats[index].caracteristics):
                    self.possible_cats[index].caracteristics[caracteristic]="otro"
                if(self.possible_cats[index].caracteristics[caracteristic]!=color.get()):
                    del self.possible_cats[index]
                    elements-=1
                else:
                    index+=1

            if(len(self.possible_cats)<2):
                other = False

        if(len(self.possible_cats) ==1):
            cattoshow = self.possible_cats[0]

            self.visual = visualizer(self.menu_window, self.frame1, cattoshow, self.rules, self)
        else:
            self.visual = visualizer(self.menu_window, self.frame1, self.default_cat, self.rules, self)

        self.visual.show()

    def show(self):
        self.title.pack()
        self.clasify()

# Oculta la vista del apartado de clasificación
    def hide(self):
        self.title.pack_forget()
        self.menuButton.pack_forget()

# Muestra la vista principal
    def main_window(self):
        self.hide()
        self.menu_window.show()

    def closing(self):
        self.visual.closing()
        del self

class main_menu:
    def __init__(self) -> None:
        openImage = Image.open("sources/cat.jpg")
        img=openImage.resize((1550, 800))
        self.frame1 = Frame(root, background='#353437')
        self.title=Label(self.frame1, text="Clasificador de razas de gatos\n\n\n", font=("Arial", 25), background='#353437', fg="white")
        self.clasifier_button=Button(self.frame1, text="Encontrar raza", command=self.show_clasifier_window, bg="#7a7b7c", fg="white")
        self.clasifier_button.config(height=5, width=30)
        self.clasifier_window=clasifier(self,self.frame1)

        # Muestra la vista principal
    def show(self):
        self.frame1.pack(pady=20)
        self.title.pack()
        self.clasifier_button.pack()

# Oculta la vista principal
    def hide(self):
        self.title.pack_forget()
        self.clasifier_button.pack_forget()

# Muestra la vista del clasificador
    def show_clasifier_window(self):
        self.hide()
        self.clasifier_window.clasify()

# Función para terminar los procesos
    def closing(self):
        self.clasifier_window.closing()
        del self

if __name__ == "__main__":
    try:
        root = Tk()
        def on_closing():
            program.closing()
            root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.title("Sistema experto de razas de gatos")
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry("%dx%d" % (w, h))
        root.configure(bg='#353437')
        program=main_menu()
        program.show()
        root.mainloop()
    except:
        quit()