import sys
import os

# Agregar el directorio padre al path para importar db
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db import Database

def consulta(query):
    db = Database()
    db.conectar()
    
    try:
      db.cursor.execute(query)
      resultados = db.cursor.fetchall()
      return resultados
    
    finally:
        db.desconectar()



prices_regular = consulta("Select min(price), max(price) from prices where fuel_type like '%regular%' ")
for precio in prices_regular:
    print(precio)



prices_premium = consulta("Select min(price), max(price) from prices where fuel_type like '%premium%' ")
for precio in prices_premium:
    print(precio)


prices_diesel = consulta("Select min(price), max(price) from prices where fuel_type like '%diesel%' ")
for precio in prices_diesel:
    print(precio)