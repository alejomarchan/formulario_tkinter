def alta(dbCon,database, titulo,descripcion):
    curs = dbCon.cursor()
    sql_alta = "insert into {}.producto (titulo, descripcion) VALUES (%s, %s)".format(database)
    data = (titulo,descripcion)
    print(sql_alta)
    curs.execute(sql_alta, data)
    dbCon.commit()

def bajas(dbCon,database, query):
    curs = dbCon.cursor()
    curs.execute(query)
    dbCon.commit()   