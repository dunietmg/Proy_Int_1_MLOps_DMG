
from typing import Union, List
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
from dateutil import parser
import pyarrow.parquet as pq
import os
import string
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


# Creacion de una aplicacion FastApi

# ejecutar: uvicorn main:app --reload   =>para cargar en el servidor


app = FastAPI()

# ------- FUNCION de bienvenida ----------
@app.get("/")
def read_root():
    return "Bienvenido al Proyecto Integrador Nro.1 de la Etapa de Labs en Henry. Autor: Duniet Marrero García"

# ------- FUNCION developer ----------

@app.get("/developer/{desarrollador}")
def developer(desarrollador: str):

    # Lee los archivos parquet de la carpeta data
    # Obtén la ruta del directorio actual del script
    current_directory = os.path.dirname(os.path.abspath(__file__))
    path_to_parquet = os.path.join(current_directory, 'data', 'df_games_etl.parquet')
    df_games_etl = pq.read_table(path_to_parquet).to_pandas()
    
    # Filtrar el DataFrame por la empresa desarrolladora
    df_desarrollador = df_games_etl[df_games_etl['developer'] == desarrollador].copy()

    def obtener_anio(fecha):
        try:
            # Intentar convertir la fecha al formato de fecha
            fecha_obj = parser.parse(fecha)
            return fecha_obj.year
        except:
            # Si no se puede convertir, retornar un valor nulo o manejarlo según sea necesario
            return None

    # Crear la columna "anio" extrayendo el año de la columna "release_date"
    df_desarrollador['anio'] = df_desarrollador['release_date'].apply(obtener_anio).astype('Int64')

    # Contar la cantidad de items por año
    cantidad_items_por_año = df_desarrollador.groupby('anio').size().reset_index(name='cantidad_items')

    # Contar la cantidad de items gratuitos por año
    cantidad_items_gratuitos_por_año = (df_desarrollador[df_desarrollador['es_gratis']].groupby('anio').size().reset_index(name='cantidad_items_gratuitos')).astype('Int64')

    # Fusionar los DataFrames para obtener la cantidad total y gratuita por año
    resultado = pd.merge(cantidad_items_por_año, cantidad_items_gratuitos_por_año, on='anio', how='left').fillna(0)

    # Calcular el porcentaje de contenido gratuito por año
    resultado['porcentaje_gratuito'] = ((resultado['cantidad_items_gratuitos'] / resultado['cantidad_items']) * 100).round(2)

    # Convertir el resultado a formato JSON para que pueda ser retornado por FastAPI
    resultado_json = resultado.to_dict(orient='records')

    return resultado_json

