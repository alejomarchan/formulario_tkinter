import mysql.connector
from mysql.connector import Error
import logging
import sys

def init():
    global db
    db = None
    try:
        logging.debug("Incio conexion a database...")
        db = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
        )
    except Error as e:
        print("Error conectando a MySQL", e)
        db = None
    else:
        print("Conexion establecida")

def createDatabase(nombre):
    #exis = False
    sql = "CREATE DATABASE {}".format(nombre)
    sql_create ="""CREATE TABLE {}.producto( id int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
                   titulo VARCHAR(128) COLLATE utf8_spanish2_ci NOT NULL, descripcion text COLLATE
                   utf8_spanish2_ci NOT NULL)""".format(nombre)
    mycursor = db.cursor(buffered=True)
    #buscarDatabase(db,nombre)
    #if not buscarDatabase(nombre):
    if not buscarDatabase(nombre):
        mycursor.execute(sql)
        mycursor.execute(sql_create)
        print("Base de datos {} Creada con exito".format(nombre))

def buscarDatabase(nombre):
    print("Ingresando en BuscarDatabase buscando {}".format(nombre))
    buscur = db.cursor(buffered=True)
    buscur.execute("show databases;", multi=True)
    while True:
        try:
            row = next(buscur)
            if nombre.lower() in row:
                return True
        except StopIteration:
            return False
            break

def deleteDatabase(nombre):
    mycursor = db.cursor()
    sql="DROP DATABASE IF EXISTS {}".format(nombre)
    mycursor.execute(sql)
    print("Delete Base de datos {} con exito".format(nombre))

def run_query(query, parametros = ()):
    mycursor = db.cursor()
    resultado = mycursor.execute(sql, parametros)
    return resultado


def close():
    db.close()
    print("Cerrando Conexion a Base de Datos")