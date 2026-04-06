import pandas as pd
import requests
import xml.etree.ElementTree as ET
import sys
import os

# Agregar el directorio padre al path para importar db
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db import Database

# URLs
PLACES_URL = "https://publicacionexterna.azurewebsites.net/publicaciones/places"
PRICES_URL = "https://publicacionexterna.azurewebsites.net/publicaciones/prices"



def get_xml(url):
    response = requests.get(url)
    return ET.fromstring(response.content)


def parsear_places(root):
    data = []

    for place in root.findall(".//place"):
        location = place.find("location")
        data.append({
            "place_id": place.get("place_id"),
            "name": place.findtext("name"),
            "lat": location.findtext("y") if location is not None else None,
            "lon": location.findtext("x") if location is not None else None,
        })


    return pd.DataFrame(data)

def parsear_prices(root):
    data = []

    for place in root.findall(".//place"):
        place_id = place.get("place_id")

        for gas in place.findall("gas_price"):
            data.append({
                "place_id": place_id,
                "fuel_type": gas.get("type"),
                "price": float(gas.text)
            })

    return pd.DataFrame(data)


def crear_tablas(db):
    """Crea las tablas si no existen"""
    db.ejecutar("""
        CREATE TABLE IF NOT EXISTS places (
            place_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            lat REAL,
            lon REAL
        )
    """)
    
    db.ejecutar("""
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            place_id TEXT NOT NULL,
            fuel_type TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)

    tablas = db.obtener_tablas()

    for tabla in tablas:
        print(tabla[0]) 
    
    print("Tablas creadas")

def load(df_places, df_prices):
    db = Database("../walmart.db")  # Guarda en backend/walmart.db
    db.conectar()
    
    try:
        # Crear tablas
        crear_tablas(db)
        
        # Limpiar datos anteriores
        db.ejecutar("DELETE FROM prices")
        db.ejecutar("DELETE FROM places")
        
        # Insertar places
        for _, row in df_places.iterrows():
            db.ejecutar("""
                INSERT OR REPLACE INTO places (place_id, name, lat, lon)
                VALUES (?, ?, ?, ?)
            """, (row['place_id'], row['name'], row['lat'], row['lon']))
            
        
        # Insertar prices
        for _, row in df_prices.iterrows():
            db.ejecutar("""
                INSERT INTO prices (place_id, fuel_type, price)
                VALUES (?, ?, ?)
            """, (row['place_id'], row['fuel_type'], row['price']))
        
        # VALIDAR DATOS INSERTADOS
        print("\n--- VALIDACIÓN ---")
        places_count = db.consultar("SELECT COUNT(*) FROM places")
        prices_count = db.consultar("SELECT COUNT(*) FROM prices")
        
        print(f"Places insertadas: {places_count[0][0]}")
        print(f"Prices insertadas: {prices_count[0][0]}")
        
        # Mostrar algunos registros
        print("\nÚltimas 3 places:")
        places_sample = db.consultar("SELECT * FROM places LIMIT 3")
        for place in places_sample:
            print(place)
        
        print("\nÚltimas 3 prices:")
        prices_sample = db.consultar("SELECT * FROM prices LIMIT 3")
        for price in prices_sample:
            print(price)
            
        print("\nDatos guardados en la base de datos")
    
    finally:
        db.desconectar()

# MAIN
if __name__ == "__main__":

    print("Extrayendo datos...")

    places_xml = get_xml(PLACES_URL)
    prices_xml = get_xml(PRICES_URL)

    print("Parseando...")
    df_places = parsear_places(places_xml)
    df_prices = parsear_prices(prices_xml)
    
    print("PLACES COLUMNS:", df_places.columns)
    print("PRICES COLUMNS:", df_prices.columns)
    
    print("Guardando en base de datos...")
    load(df_places, df_prices)

    print("ETL completo")

   