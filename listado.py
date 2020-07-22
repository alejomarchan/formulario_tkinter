class listado():
    def listar(self, dbCon,database,tabla):
        curs = dbCon.cursor(buffered=True)
        sql = "select * from {}.{} order by 1".format(database,tabla)
        curs.execute(sql)
        data = curs.fetchall()
        return data
    
    def alta(self, dbCon,database, titulo,descripcion):
        curs = dbCon.cursor()
        sql_alta = "insert into {}.producto (titulo, descripcion) VALUES (%s, %s)".format(database)
        data = (titulo,descripcion)
        print(sql_alta)
        curs.execute(sql_alta, data)
        dbCon.commit()
        print("Alta exitosa")