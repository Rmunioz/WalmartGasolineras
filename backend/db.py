import sqlite3

class Database:
    def __init__(self, db_name="walmart.db"):
        self.db_name = db_name
        self.con = None
        self.cursor = None
    
    def conectar(self):
        self.con = sqlite3.connect(self.db_name)
        self.cursor = self.con.cursor()
    
    def desconectar(self):
        if self.con:
            self.con.close()
    
    def ejecutar(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.con.commit()
    
    def obtener_tablas(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return self.cursor.fetchall()
    
    def consultar(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()


