# Walmart Gasolineras

Este proyecto que fue solicitado como caso de uso, muestra los productos (combustibles: Diésel, Regular y Premium) vendido en las gasolineras Walmart del país.

Este proyecto es un ETL.
Se leen los datos de las siguientes rutas:
- https://publicacionexterna.azurewebsites.net/publicaciones/places
- https://publicacionexterna.azurewebsites.net/publicaciones/prices

Se hace la transformación necesaria de esta información para cumplir con los requisitos necesarios que se piden en el caso de uso.
Se hace la carga de esta información en base de datos (sqlite3)


# Lenguajes usados:
- Frontend: Javascript (React)
- Backend: Python

# Librerías, frameworks principales:
- numpy
- flask
- haversine
- BallTree
- geopandas
- react-leaflet


# Requerimientos para levantar este proyecto.
- Python 3.9.6
- pip 26.0.1
- nodeJs v24.13.0
- En mac sqlite3 ya viene preinstalado, de usar otro S.O instalar sqlite3

# Comandos para levantar el proyecto
- En la carpeta backend: python3 main.py
- En la carpeta frontend: npm run dev

# GITHUB
- https://chatgpt.com/c/69d3e700-7e94-83e8-923e-e60b4b745615


