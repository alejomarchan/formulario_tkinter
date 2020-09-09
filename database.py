import mysql.connector
from mysql.connector import Error
import logging
import sys

class DatabaseClass:
    """Esta clase se encarga de gestionar las conexiones y
        las actividades relaciones con los DML y DDL del
        proceso"""
    def __init__(self):
        """El Init se encarga de realizar la conexión una
            vezz instanciado el objeto de la Clase DatabaseClass"""
        global db
        self.db = None
        try:
            logging.debug("Incio conexion a database...")
            self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
            )
        except Error as e:
            print("Error conectando a MySQL", e)
            self.db = None
        else:
            print("Conexion establecida")

    def createDatabase(self,nombre):
        """Funcion que crea la base de datos en Mysql
            Parameters
            ----------
            nombre : str
                Es el nombre que se le asigna a la base de datos cuando es creada"""
        #exis = False
        sql = "CREATE DATABASE {}".format(nombre)
        sql_create ="""CREATE TABLE {}.producto( id int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
                    titulo VARCHAR(128) COLLATE utf8_spanish2_ci NOT NULL, descripcion text COLLATE
                    utf8_spanish2_ci NOT NULL)""".format(nombre)
        mycursor = self.db.cursor(buffered=True)
        #buscarDatabase(db,nombre)
        #if not buscarDatabase(nombre):
        if not self.buscarDatabase(nombre):
            mycursor.execute(sql)
            mycursor.execute(sql_create)
            print("Base de datos {} Creada con exito".format(nombre))

    def buscarDatabase(self,nombre):
        """Funcion que busca si la base de datos nombre existe en Mysql
                    Parameters
                    ----------
                    nombre : str
                        Es el nombre es el esquema de la Base de Datos que queremos
                        revisar si existe en Mysql

                    Return
                    ----------
                        True si la Base de Datos existe
                        False si la Base de Datos no existe
                    """
        print("Ingresando en BuscarDatabase buscando {}".format(nombre))
        buscur = self.db.cursor(buffered=True)
        buscur.execute("show databases;", multi=True)
        while True:
            try:
                row = next(buscur)
                if nombre.lower() in row:
                    return True
            except StopIteration:
                return False
                break

    def deleteDatabase(self,nombre):
        """Funcion que elimina la base de datos nombre (si existe en Mysql)
               Parameters
               ----------
               nombre : str
                   Es el nombre es el esquema de la Base de Datos que queremos
                   eliminar
               """
        mycursor = self.db.cursor()
        sql = "DROP DATABASE IF EXISTS {}".format(nombre)
        mycursor.execute(sql)
        print("Delete Base de datos {} con exito".format(nombre))

    def run_query(self,query, parametros = ()):
        """Funcion que ejecuta el comando juntos con sus parámetros
               Parameters
               ----------
               query : str
                   Es el sql a ejecutar
               parametros : lis
                   Son el conjunto de valores que puede tomar el filtro del sql

               Return
               ----------
                   resultado que es el cursor que devuelve la ejecución del SQL
               """
        mycursor = self.db.cursor()
        resultado = mycursor.execute(query, parametros)
        return resultado


    def close(self):
        """Funcion que cierra la conexión establecida a la base de datos
                       """
        self.db.close()
        print("Cerrando Conexion a Base de Datos")