class Administradora:
    """Esta clase se encarga de gestionar los registros que se encuentren
        almacenados en la Base de Datos para mostrarlos en la ventana
        destinada para tal fin en el Tkinter.
        También con esta clase se pueden gestionar las altas de nuevos elementos,
        modificaciones de los ya existen y la eliminacion de los registros almacenados"""
    def alta(self, dbCon, database, titulo, descripcion):
        """Funcion que busca si la base de datos nombre existe en Mysql
            Parameters
            ----------
            dbCon : object
                Es el objeto instanciado con la conexión estableciada de la Base de Datos
            database : string
                Es el nombre de la Base de Datos en Mysql
            titulo : string
                Es la cadena que contiene el valor ingresado en la ventana del Tkinter
                en el campo Titulo
            descripcion : string
                Es la cadena que contiene el valor ingresado en la ventana del Tkinter
                en el campo descripcion

            Return
            ----------
                True si la Base de Datos existe
                False si la Base de Datos no existe
            """
        curs = dbCon.cursor()
        sql_alta = "insert into {}.producto (titulo, descripcion) VALUES (%s, %s)".format(database)
        data = (titulo,descripcion)
        print(sql_alta)
        curs.execute(sql_alta, data)
        dbCon.commit()

    def bajas(self,dbCon, database, query):
        """Funcion que busca si la base de datos nombre existe en Mysql
            Parameters
            ----------
            dbCon : object
                Es el objeto instanciado con la conexión estableciada de la Base de Datos
            database : string
                Es el nombre de la Base de Datos
            query : string
                Es el DML generado para el delete del registro
            """
        curs = dbCon.cursor()
        curs.execute(query)
        dbCon.commit()

    def listar(self, dbCon, database, tabla):
        """Funcion que lista los registros que se encuentren almacenados en la tabla de Base de Datos
            Parameters
            ----------
            dbCon : object
                Es el objeto instanciado con la conexión estableciada de la Base de Datos
            database : string
                Es el nombre de la Base de Datos
            tabla : string
                Es la tabla donde se encuentran almacenados los registros

            return
            ----------
            data : cursor
                Los valores del fetch del sql
            """
        curs = dbCon.cursor(buffered=True)
        sql = "select * from {}.{} order by 1".format(database,tabla)
        curs.execute(sql)
        data = curs.fetchall()
        return data