
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

# ------- FUNCION userdata ----------

@app.get("/userdata/{user_id}")
def userdata(user_id: str):

    # Lee los archivos parquet de la carpeta data
    current_directory = os.path.dirname(os.path.abspath(__file__))
    path_to_parquet = os.path.join(current_directory, 'data', 'df_gastos_items.parquet')
    df_gastos_items = pq.read_table(path_to_parquet).to_pandas()
    
    current_directory = os.path.dirname(os.path.abspath(__file__))
    path_to_parquet = os.path.join(current_directory, 'data', 'df_reviews_etl.parquet')
    df_reviews_etl = pq.read_table(path_to_parquet).to_pandas()
    

    # Filtra por el usuario de interés
    usuario = df_reviews_etl[df_reviews_etl['user_id'] == user_id]
    
    if usuario.empty:
        raise HTTPException(status_code=404, detail="User not found")

    # Convertir user_id a tipo string para asegurarse de que coincida con el tipo de datos en los DataFrames
    user_id = str(user_id)

    # Calcula la cantidad de dinero gastado para el usuario de interés
    cantidad_dinero = df_gastos_items[df_gastos_items['user_id'] == user_id]['price'].iloc[0]
    
    # Busca el count_item para el usuario de interés
    count_items = df_gastos_items[df_gastos_items['user_id'] == user_id]['items_count'].iloc[0]

    # Calcula el total de recomendaciones realizadas por el usuario de interés
    total_recomendaciones = usuario['recommend'].sum()
    
    # Calcula el total de reviews realizada por todos los usuarios
    total_reviews = len(df_reviews_etl['user_id'].unique())
    
    # Calcula el porcentaje de recomendaciones realizadas por el usuario de interés
    porcentaje_recomendaciones = (total_recomendaciones / total_reviews) * 100

    return {
        'cantidad_dinero': int(cantidad_dinero),
        'porcentaje_recomendacion': round(float(porcentaje_recomendaciones), 2),
        'total_items': int(count_items)
    }

# ------- FUNCION user_for_genre ----------

@app.get("/user_for_genre/{genre}", response_model=dict)
def user_for_genre(genre: str):

    # Lee el archivo parquet de la carpeta data
    current_directory = os.path.dirname(os.path.abspath(__file__))
    path_to_parquet = os.path.join(current_directory, 'data', 'df_games_genres.parquet')
    df_games_genres = pq.read_table(path_to_parquet).to_pandas()
    
    current_directory = os.path.dirname(os.path.abspath(__file__))
    path_to_parquet = os.path.join(current_directory, 'data', 'df_users_horas.parquet')
    df_users_horas = pq.read_table(path_to_parquet).to_pandas()

    # Une ambos dataframes
    df_genres_horas = df_games_genres.merge(df_users_horas, on='item_id', how='right')

    # Filtra el DataFrame resultante para obtener solo las filas relacionadas con el género dado
    df_filtered = df_genres_horas[df_genres_horas['genres'] == genre]

    if df_filtered.empty:
        return {"message": "No data found for the given genre"}

    # Encontrar el usuario que acumula más horas jugadas para el género dado
    max_user = df_filtered.groupby('user_id')['playtime_forever'].sum().idxmax()

    # Filtrar el DataFrame para obtener solo las filas relacionadas con el usuario que acumula más horas
    df_user_max_hours = df_filtered[df_filtered['user_id'] == max_user]

    # Agrupar por año y sumar las horas jugadas
    horas_por_anio = df_user_max_hours.groupby('anio')['playtime_forever'].sum()

    # Construir el diccionario de resultados
    result_dict = {
        "Usuario con más horas jugadas para Género X": max_user,
        "Horas jugadas": [{"Año": int(year), "Horas": int(hours)} for year, hours in horas_por_anio.reset_index().to_dict(orient='split')['data']]
    }

    return result_dict

# ------- FUNCION best_developer_year ----------


# Definir la ruta de FastAPI para la función best_developer_year
@app.get("/best_developer/{year}", response_model=List[dict])

def best_developer_year(year: int):

    # Lee el archivo parquet de la carpeta data
    current_directory = os.path.dirname(os.path.abspath(__file__))
    path_to_parquet = os.path.join(current_directory, 'data', 'df_best_developer_anio.parquet')
    df_best_developer_anio = pq.read_table(path_to_parquet).to_pandas()

    # Filtra el DataFrame para el año dado y donde recommend es True y sentiment_analysis es positivo
    df_filtered = df_best_developer_anio[(df_best_developer_anio['anio'] == year) &
                                         (df_best_developer_anio['recommend'] == True) &
                                         (df_best_developer_anio['sentiment_analysis'] > 1)]

    if df_filtered.empty:
        return None

    # Agrupar por desarrollador y contar la cantidad de juegos recomendados
    top_developers = df_filtered.groupby('developer')['recommend'].sum().nlargest(3)

    # Construir el resultado como una lista de diccionarios
    result = [{"Top {}".format(i + 1): developer} for i, (developer, _) in enumerate(top_developers.items())]

    return result


