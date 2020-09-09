import validador as vl
import tkinter as tk
from tkinter import messagebox, ttk
import database
import altas
import temas


#Nombre Base de Datos
nameDatabase="alejandro"

#Iniciando conexión a la Base de Datos
#database.init()
#lista = lst.listado()
#val = vl.Valida()

class Titulo:
    def __init__(self, vent_par):
        #Nombre Base de Datos
        self.nameDatabase="alejandro"
        self.ventana = vent_par
        self.ventana.title("Tarea Tres POO")
        self.val = vl.Valida()
        self.ddbb = database.DatabaseClass()
        self.alta = altas.Administradora()

        #Creando el contenedor
        formulario = tk.LabelFrame(self.ventana, text = 'Ingrese Producto',fg="white", bg="darkorchid3")
        formulario.grid(row = 0, column = 0, columnspan= 3, pady = 20)

        #Creando las etiquetas del Titulo
        tk.Label(formulario ,text = "Titulo").grid(row = 1,column = 0)
        self.titulo = tk.Entry(formulario)
        self.titulo.focus()
        self.titulo.grid(row = 1, column = 1)

        #Creando las etiquetas de la Descripción
        tk.Label(formulario ,text = "Descripcion").grid(row = 2,column = 0)
        self.descripcion = tk.Entry(formulario)
        self.descripcion.grid(row = 2, column = 1)
        
        #Creando las Botones Alta y Creacion Database
        button_alta = tk.Button(formulario, text="Alta", command=self.checkAlta, height=1, width=12).grid(row=6, columnspan = 8, sticky= 'e')
        button_creardb = tk.Button(formulario, text="Crear DB", command=self.crearDb, height=1, width=12).grid(row=6, columnspan = 8, sticky= 'w')


        #Creando la lista de los valores ingresados
        self.lista = ttk.Treeview(height = 10 ,columns = ("#0","#1","#2"))
        self.lista.grid(row = 4, column = 0, columnspan = 2)
        self.lista.heading("#0",text="ID",anchor="center")
        self.lista.heading("#1",text="Titulo",anchor="center")
        self.lista.heading("#2",text="Descripcion",anchor="center")
        self.getLista()
        
        #Creando las Botones Update y Delete
        button_delete = tk.Button(text="Borrar",command = self.borrarDato, height=1, width=12).grid(row=5, column = 0, sticky= 'we')
        button_update = tk.Button(text="Actualizar", command = self.updateData, height=1, width=12).grid(row=5, column = 1, sticky= 'we')

        #Creando los Radiobutton para el cambio de color del background
        tk.Label(formulario ,text = "Temas",bg="cyan",fg="black",height=1,width=24).grid(row = 7,columnspan=5)
        val_boton = tk.IntVar()
        rad_but1 = tk.Radiobutton(formulario, text="Color 1", fg="black",variable=val_boton, value=1, command = lambda:temas.EleccionTema(formulario,val_boton.get()))
        rad_but1.grid(row=11, column=0, columnspan=5)
        rad_but1.config(bg ="grey")
        rad_but2 = tk.Radiobutton(formulario, text="Color 2",fg="grey", variable=val_boton, value=2, command = lambda:temas.EleccionTema(formulario,val_boton.get()))
        rad_but2.grid(row=12, column=0, columnspan=5)
        rad_but2.config(bg ="black")
        rad_but3 = tk.Radiobutton(formulario, text="Color 3",fg="grey", variable=val_boton, value=3, command = lambda:temas.EleccionTema(formulario,val_boton.get()))
        rad_but3.grid(row=13, column=0, columnspan=5)
        rad_but3.config(bg ="black")
        
        button_delete = tk.Button(text="Borrar",command = self.borrarDato, height=1, width=12).grid(row=5, column = 0, sticky= 'we')
        button_update = tk.Button(text="Actualizar", command = self.updateData, height=1, width=12).grid(row=5, column = 1, sticky= 'we')


    def getLista(self):
        #Acá me traigo todos los elementos almacenados en la base de datos
        self.data = self.alta.listar(self.ddbb.db,nameDatabase,'producto')

        #Acá procedo a obtener los hijos de la tabla, borrarlos
        registros = self.lista.get_children()
        for registro in registros:
            self.lista.delete(registro)

        #Con el siguiente For procedo a llenar la vista del arbol
        for row in self.data:
            self.lista.insert("", "end", text=str(row[0]), values=(row[1], row[2]))
        

    def checkAlta(self):
        if self.val.validar(self.descripcion.get()):
            if not self.ddbb.buscarDatabase(nameDatabase):
                #La base de datos no existe y la creo en el alta
                self.crearDb()
            #Ingresando valor a la Base de datos
            self.alta.alta(self.ddbb.db,nameDatabase,self.titulo.get(),self.descripcion.get())
            self.getLista()
            self.titulo.delete(0, tk.END)
            self.descripcion.delete(0, tk.END)
            self.titulo.focus()
        else:
            messagebox.showerror(message="El Titulo que ingreso no cumple con los requisitos de caracteres y no es valido",title="Error")


    def crearDb(self):
        if self.ddbb.buscarDatabase(nameDatabase):
            confirm = messagebox.askyesno(
                  title="Base de Datos {} Existente".format(self.nameDatabase),
                  message="Seguro que la desea Recrear?",
                  default=messagebox.NO)
        if (confirm==True): 
            self.ddbb.deleteDatabase(self.nameDatabase)
            self.ddbb.createDatabase(self.nameDatabase)
        
        self.getLista()
        return

    def borrarDato(self):
        try:
            self.lista.item(self.lista.selection())['text'][0]
        except IndexError as e:
            messagebox.showerror(message="Selecciona un registro",title="Error")
            return
        confirm = messagebox.askyesno(
                  title="Borrar Elemento",
                  message="Seguro que desea elimar el elemento?",
                  default=messagebox.NO)
        if (confirm==True):
            query = "delete from {}.producto where id ={}".format(self.nameDatabase ,self.lista.item(self.lista.selection())['text'][0])
            self.alta.bajas(self.ddbb.db,nameDatabase,query)
        self.getLista()      
        return

    def updateData(self):
        try:
            self.lista.item(self.lista.selection())['text'][0]
        except IndexError as e:
            messagebox.showerror(message="Selecciona un registro",title="Error")
            return
        indice = self.lista.item(self.lista.selection())['text'][0]
        print("En el Update Data del indice {}".format(indice))
        print(self.lista.item(self.lista.selection()))
        old_tit = self.lista.item(self.lista.selection())['values'][0]
        old_desc = self.lista.item(self.lista.selection())['values'][1]
        self.ventana_edi = tk.Toplevel()
        self.ventana_edi.title = "Editar elemento"
        #Valor Titulo antiguo
        tk.Label(self.ventana_edi, text = 'Titulo Anterior').grid(row = 0, column =1)
        tk.Entry(self.ventana_edi, textvariable = tk.StringVar(self.ventana_edi, value = old_tit), state = 'readonly').grid(row= 0, column = 2)
        #Valor Titulo nuevos
        tk.Label(self.ventana_edi, text = 'Titulo Nuevo').grid(row = 1, column =1)
        new_title = tk.Entry(self.ventana_edi)
        new_title.grid(row= 1, column = 2)

        #Valor Descripcion antigua
        tk.Label(self.ventana_edi, text = 'Descripcion Anterior').grid(row = 2, column = 1)
        tk.Entry(self.ventana_edi, textvariable = tk.StringVar(self.ventana_edi, value = old_desc), state = 'readonly').grid(row= 2, column = 2)
        #Valor Descripcion Nueva
        tk.Label(self.ventana_edi, text = 'Descripcion Nueva').grid(row = 3, column =1)
        new_descr = tk.Entry(self.ventana_edi)
        new_descr.grid(row= 3, column = 2)
        print("En el Boton del Update Data")
        #tk.Button(self.ventana_edi, text="Actualizar", height=1, width=12).grid(row=4, column = 2, sticky= 'we')     
        #query = "update {}.producto set titulo = {}, descripcion = {} where id ={}".format(self.nameDatabase, new_tit.get(), new_desc.get(), self.lista.item(self.lista.selection())['text'][0])
        #print(query)
        #altas.bajas(database.db,nameDatabase,query)
        tk.Button(self.ventana_edi, text="Actualizar",command = lambda: self.actualiza(nameDatabase, new_title.get(), new_descr.get(), indice), height=1, width=12).grid(row=4, column = 2, sticky= 'we')

        
        self.getLista()      
        return

    def actualiza(self,databasename, nuevo_titulo, nueva_descripcion, id_reg):
        if self.val.validar(nuevo_titulo):
            query = "update {}.producto set titulo = '{}', descripcion = '{}' where id ={}".format(databasename, nuevo_titulo, nueva_descripcion, id_reg)
            print(query)
            self.alta.bajas(self.ddbb.db,nameDatabase,query)
            self.ventana_edi.destroy()
        else:
            messagebox.showerror(message="El Titulo que ingreso no cumple con los requisitos de caracteres y no es valido",title="Error")
        self.getLista()