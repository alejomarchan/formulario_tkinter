import validador as vl
import tkinter as tk
from tkinter import messagebox, ttk
import database
import altas
import listado as lst


#Nombre Base de Datos
nameDatabase="alejandro"

#Iniciando conexión a la Base de Datos
database.init()
lista = lst.listado()
val = vl.Valida()

class Titulo:
    def __init__(self, vent_par):
        #Nombre Base de Datos
        self.nameDatabase="alejandro"
        self.ventana = vent_par
        self.ventana.title("Tarea POO")

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


    def getLista(self):
        #Acá me traigo todos los elementos almacenados en la base de datos
        self.data = lista.listar(database.db,nameDatabase,'producto')

        #Acá procedo a obtener los hijos de la tabla, borrarlos
        registros = self.lista.get_children()
        for registro in registros:
            self.lista.delete(registro)

        #Con el siguiente For procedo a llenar la vista del arbol
        for row in self.data:
            self.lista.insert("", "end", text=str(row[0]), values=(row[1], row[2]))
        

    def checkAlta(self):
        if val.validar(self.descripcion.get()):
            if not database.buscarDatabase(nameDatabase):
                #La base de datos no existe y la creo en el alta
                self.crearDb()
            #Ingresando valor a la Base de datos
            altas.alta(database.db,nameDatabase,self.titulo.get(),self.descripcion.get())
            self.getLista()
            self.titulo.delete(0, tk.END)
            self.descripcion.delete(0, tk.END)
            self.titulo.focus()
        else:
            messagebox.showerror(message="El Titulo que ingreso no cumple con los requisitos de caracteres y no es valido",title="Error")


    def crearDb():
        database.deleteDatabase(self.nameDatabase)
        database.createDatabase(self.nameDatabase)

    def borrarDato(self):
        try:
            self.lista.item(self.lista.selection())['text'][0]
        except IndexError as e:
            messagebox.showerror(message="Selecciona un registro",title="Error")
            return
        query = "delete from {}.producto where id ={}".format(self.nameDatabase ,self.lista.item(self.lista.selection())['text'][0])
        altas.bajas(database.db,nameDatabase,query)
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
        query = "update {}.producto set titulo = '{}', descripcion = '{}' where id ={}".format(databasename, nuevo_titulo, nueva_descripcion, id_reg)
        print(query)
        altas.bajas(database.db,nameDatabase,query)
        self.ventana_edi.destroy()
        self.getLista()




if __name__ == '__main__':
    ventana = tk.Tk()
    aplicacion = Titulo(ventana)
    ventana.mainloop()
    if database.db is not None:
        print("Conexion funcionando")
        database.close()
    else:
        print("No hubo conexion abierta")