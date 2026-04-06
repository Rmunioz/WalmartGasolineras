from flask import Flask, jsonify, request
from flask_cors import CORS
from db import Database
from haversine import haversine, Unit
from sklearn.neighbors import BallTree
import numpy as np
import geopandas as gpd
from shapely.geometry import Point  
   
app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    return response

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({"status": "ok", "message": "servidor funcionando"})

@app.route('/api/states-saturation', methods=['GET'])
def get_states_saturation():
    try:
    
        mexico = gpd.read_file("estadosMexico.json")

        if mexico.crs != "EPSG:4326":
            mexico = mexico.to_crs("EPSG:4326")

        db = Database()
        db.conectar()
        places = db.consultar("""
            SELECT place_id, name, lat, lon 
            FROM places 
            WHERE lat IS NOT NULL AND lon IS NOT NULL
        """)
        db.desconectar()

        stations_gdf = gpd.GeoDataFrame(
            places,
            geometry=[Point(lon, lat) for _, _, lat, lon in places],
            crs="EPSG:4326"
        )

       
        joined = gpd.sjoin(stations_gdf, mexico, how="left", predicate="within")

      
        saturation = joined.groupby("name").size().reset_index(name="saturation")

        mexico_with_sat = mexico.merge(saturation, on="name", how="left")
        mexico_with_sat["saturation"] = mexico_with_sat["saturation"].fillna(0)

        result = []
        for _, row in mexico_with_sat.iterrows():
            result.append({
                "state": row["name"],
                "saturation": int(row["saturation"]),
                "geometry": row["geometry"].__geo_interface__
            })

        return jsonify(result)

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500
    

@app.route('/api/stations', methods=['GET', 'OPTIONS'])
def get_stations():
    try:

        #OFFSET VARIABLE PARA PAGINACIÓN Y NO SOBRECARGAR EL SERVIDOR
        limit = int(request.args.get("limit", 200))
        offset = int(request.args.get("offset", 0))
        if limit < 1:
            limit = 200
        if offset < 0:
            offset = 0

        db = Database()
        db.conectar()
        
        # JOIN entre places y prices
        query = """
            SELECT 
                p.place_id,
                p.name,
                p.lat,
                p.lon,
                pr.fuel_type,
                pr.price
            FROM places p
            LEFT JOIN prices pr ON p.place_id = pr.place_id
            ORDER BY p.place_id
            LIMIT ? OFFSET ?
        """
        
        results = db.consultar(query, (limit, offset))
        
        # Devolver todos los registros sin agrupar
        stations = []
        for row in results:
            place_id, name, lat, lon, fuel_type, price = row
            stations.append({
                "place_id": place_id,
                "name": name,
                "lat": lat,
                "lon": lon,
                "fuel_type": fuel_type,
                "price": price
            })
        
        db.desconectar()
        return jsonify(stations)
    
    except Exception as e:
        print(f"Error en /api/stations: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/prices', methods=['GET', 'OPTIONS'])
def get_prices():
    db = Database()
    db.conectar()
    
    try:
        results = db.consultar("SELECT * FROM prices")
        return jsonify(results)
    finally:
        db.desconectar()

@app.route('/api/places', methods=['GET', 'OPTIONS'])
def get_places():
    db = Database()
    db.conectar()
    
    try:
        results = db.consultar("SELECT * FROM places")
        return jsonify(results)
    finally:
        db.desconectar()

@app.route('/api/top-neighboring-stations', methods=['GET'])
def get_top_neighboring_stations():
    try:
        db = Database()
        db.conectar()

        places = db.consultar("""
            SELECT place_id, name, lat, lon 
            FROM places 
            WHERE lat IS NOT NULL AND lon IS NOT NULL
        """)

        if not places:
            return jsonify([])

        # Convertir a numpy
        coords = np.array([[p[2], p[3]] for p in places])
        coords_rad = np.radians(coords)

        # Crear arbol
        tree = BallTree(coords_rad, metric='haversine')

        # 3 km en radianes
        radius = 3 / 6371

        # Contar vecinos
        counts = tree.query_radius(coords_rad, r=radius, count_only=True)

        results = []
        for i, place in enumerate(places):
            place_id, name, lat, lon = place

            results.append({
                "place_id": place_id,
                "name": name,
                "lat": lat,
                "lon": lon,
                "neighbors_count": int(counts[i] - 1)  # quita el suyo
            })

        top_10 = sorted(results, key=lambda x: x['neighbors_count'], reverse=True)[:10]

        return jsonify(top_10)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        db.desconectar()

if __name__ == '__main__':
    app.run(debug=True, port=4000)
