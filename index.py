import ventana as vtn

if __name__ == '__main__':
    ventana = vtn.tk.Tk()
    aplicacion = vtn.Titulo(ventana)
    ventana.mainloop()
    if aplicacion.ddbb.db is not None:
        print("Conexion funcionando")
        aplicacion.ddbb.close()
    else:
        print("No hubo conexion abierta")