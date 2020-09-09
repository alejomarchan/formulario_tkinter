class listado():
    """Esta clase se encarga de listar los registros que se encuentren
        almacenados en la Base de Datos para mostrarlos
        en la ventana destinada para tal fin en el Tkinter"""
    def alta(self, dbCon,database, titulo,descripcion):
        curs = dbCon.cursor()
        sql_alta = "insert into {}.producto (titulo, descripcion) VALUES (%s, %s)".format(database)
        data = (titulo,descripcion)
        print(sql_alta)
        curs.execute(sql_alta, data)
        dbCon.commit()
        print("Alta exitosa")