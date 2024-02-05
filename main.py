# LIBRERÍAS

from typing import Union, List
import os
import string
import re
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from dateutil import parser
import pandas as pd
import pyarrow.parquet as pq
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier



# ejecutar: uvicorn main:app --reload   =>para cargar en el servidor

app = FastAPI()

#  => FUNCION INICIO 

@app.get("/")
def read_root():
    welcome_message = "Bienvenido al Proyecto Integrador Nro.1 de la Etapa de Labs en Henry. Autor: Duniet Marrero García. "
    additional_message = "Para continuar y explorar las funciones de la API, agregue /docs al final de la URL."
    return welcome_message + additional_message



# => FUNCION DEVELOPER

@app.get("/developer/{desarrollador}")
def developer(desarrollador: str):

    # Lee el archivo parquet y obtiene la ruta del directorio actual del script
    current_directory = os.path.dirname(os.path.abspath(__file__))
    path_to_parquet = os.path.join(current_directory, 'data', 'df_steam_games.parquet')
    df_steam_games = pq.read_table(path_to_parquet).to_pandas()
    
    # Filtra el dataframe por la empresa desarrolladora
    df_desarrollador = df_steam_games[df_steam_games['developer'] == desarrollador].copy()

    def obtener_anio(fecha):
        try:
            # Convierte la fecha al formato correcto
            fecha_obj = parser.parse(fecha)
            return fecha_obj.year
        except:
            return None

    # Crea la columna "anio" a partir de la columna "release_date"
    df_desarrollador['anio'] = df_desarrollador['release_date'].apply(obtener_anio).astype('Int64')

    # Cantidad de items por año
    cantidad_items_por_año = df_desarrollador.groupby('anio').size().reset_index(name='cantidad_items')

    # Cantidad de items gratuitos por año
    cantidad_items_gratuitos_por_año = (df_desarrollador[df_desarrollador['es_gratis']].groupby('anio').size().reset_index(name='cantidad_items_gratuitos')).astype('Int64')

    # Une los dataframes 
    resultado = pd.merge(cantidad_items_por_año, cantidad_items_gratuitos_por_año, on='anio', how='left').fillna(0)

    # Porcentaje de contenido gratuito por año
    resultado['porcentaje_gratuito'] = ((resultado['cantidad_items_gratuitos'] / resultado['cantidad_items']) * 100).round(2)

    # Convierte el resultado a formato JSON
    resultado_json = resultado.to_json(orient='records')

    return JSONResponse(content=resultado_json)
    

# => FUNCION USERDATA

@app.get("/userdata/{user_id}")
def userdata(user_id: str):

    # Lee los archivos parquet y obtiene la ruta del directorio actual del script
    current_directory = os.path.dirname(os.path.abspath(__file__))
    path_to_parquet = os.path.join(current_directory, 'data', 'df_items_userdata.parquet')
    df_items_userdata = pq.read_table(path_to_parquet).to_pandas()
    
    current_directory = os.path.dirname(os.path.abspath(__file__))
    path_to_parquet = os.path.join(current_directory, 'data', 'df_reviews_userdata.parquet')
    df_reviews_userdata = pq.read_table(path_to_parquet).to_pandas()
    

    # Filtra por el usuario de interés
    usuario = df_reviews_userdata[df_reviews_userdata['user_id'] == user_id]
    
    if usuario.empty:
        raise HTTPException(status_code=404, detail="User not found")

    # Convierte user_id a tipo string 
    user_id = str(user_id)

    # Cantidad de dinero gastado por el usuario 
    cantidad_dinero = df_items_userdata[df_items_userdata['user_id'] == user_id]['price'].iloc[0]
    
    # Cantidad de item para el usuario 
    count_items = df_items_userdata[df_items_userdata['user_id'] == user_id]['items_count'].iloc[0]

    # Total de recomendaciones realizadas por el usuario
    total_recomendaciones = usuario['recommend'].sum()
    
    # Total de reviews realizados por todos los usuarios
    total_reviews = len(df_reviews_userdata['user_id'].unique())
    
    # Porcentaje de recomendaciones realizadas por el usuario
    porcentaje_recomendaciones = (total_recomendaciones / total_reviews) * 100

    return {
        'cantidad_dinero': int(cantidad_dinero),
        'porcentaje_recomendacion': round(float(porcentaje_recomendaciones), 2),
        'total_items': int(count_items)
    }


# => FUNCION USER_FOR_GENRE

@app.get("/user_for_genre/{genre}", response_model=dict)
def user_for_genre(genre: str):

    # Lee el archivo parquet y obtiene la ruta del directorio actual del script
    current_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Carga los datos de juegos y géneros
    path_to_games_parquet = os.path.join(current_directory, 'data', 'df_games_user_genre.parquet')
    df_games_user_genre = pq.read_table(path_to_games_parquet).to_pandas()
    
    # Carga los datos de usuarios y horas jugadas
    path_to_users_parquet = os.path.join(current_directory, 'data', 'df_user_horas_juego.parquet')
    df_user_horas_juego = pq.read_table(path_to_users_parquet).to_pandas()

    # Une ambos dataframes
    df_genres_hours = df_games_user_genre.merge(df_user_horas_juego, on='item_id', how='right')

    # Filtra el dataframe para obtener solo las filas relacionadas con el género dado
    df_filtered = df_genres_hours[df_genres_hours['genres'] == genre]

    if df_filtered.empty:
        raise HTTPException(status_code=404, detail="No data found for the given genre")

    # Encuentra el usuario que acumula más horas jugadas para el género
    max_user = df_filtered.groupby('user_id')['playtime_forever'].sum().idxmax()

    # Filtra el dataframe para obtener solo las filas relacionadas con el usuario que acumula más horas
    df_user_max_hours = df_filtered[df_filtered['user_id'] == max_user]

    # Agrupa por año y suma las horas jugadas
    horas_por_anio = df_user_max_hours.groupby('anio')['playtime_forever'].sum()

    # Construiye el diccionario de resultados
    result_dict = {
        "Usuario con más horas jugadas para Género X": max_user,
        "Horas jugadas": [{"Año": int(year), "Horas": int(hours)} for year, hours in horas_por_anio.reset_index().to_dict(orient='split')['data']]
    }

    result_json = jsonable_encoder(result_dict)
    return JSONResponse(content=result_json)

    

# => FUNCION BEST_DEVELOPER_YEAR


@app.get("/best_developer_year/{anio}", response_model=List[dict])

def best_developer_year(anio: int):

    # Lee el archivo parquet y obtiene la ruta del directorio actual del script
    current_directory = os.path.dirname(os.path.abspath(__file__))
    path_to_parquet = os.path.join(current_directory, 'data', 'df_best_developer_anio.parquet')
    df_best_developer_anio = pq.read_table(path_to_parquet).to_pandas()

    # Filtra el dataframe para el año dado y donde recommend es True y sentiment_analysis es positivo
    df_filtered = df_best_developer_anio[(df_best_developer_anio['anio'] == anio) &
                                         (df_best_developer_anio['recommend'] == True) &
                                         (df_best_developer_anio['sentiment_analysis'] > 1)]

    if df_filtered.empty:
        return None

    # Agrupa por desarrollador y cuenta la cantidad de juegos recomendados
    top_developers = df_filtered.groupby('developer')['recommend'].sum().nlargest(3)

    # Construye el resultado como una lista de diccionarios
    result = [{"Top {}".format(i + 1): developer} for i, (developer, _) in enumerate(top_developers.items())]

    return result


# => FUNCION DEVELOPER_REVIEWS_ANALYSIS

@app.get("/developer-reviews-analysis/{desarrollador}")
def developer_reviews_analysis_endpoint(desarrollador: str):

    # Lee el archivo parquet y obtiene la ruta del directorio actual del script
    current_directory = os.path.dirname(os.path.abspath(__file__))
    path_to_parquet = os.path.join(current_directory, 'data', 'df_developer_review.parquet')
    df_developer_review = pq.read_table(path_to_parquet).to_pandas()
    

    # Filtra el dataframe para el desarrollador dado
    df_filtered = df_developer_review[df_developer_review['developer'] == desarrollador]

    
    if df_filtered.empty:
        raise HTTPException(status_code=404, detail=f"No se encontraron registros para el desarrollador {desarrollador}")

    # Agrupa por análisis de sentimiento y cuenta la cantidad de registros
    analysis_counts = df_filtered.groupby('sentiment_analysis').size().to_dict()

    # Construye el resultado como un diccionario con una lista
    result = {desarrollador: [f'Negative = {analysis_counts.get(0, 0)}', f'Positive = {analysis_counts.get(2, 0)}']}

    return result


# => ML MODELO DE RECOMENDACION - TITULOS DE JUEGOS SIMILARES

@app.get("/recomendacion_juego/{titulo}")
def get_recomendacion_juego(titulo: str):
    
    # Lee el archivo parquet y obtiene la ruta del directorio actual del script
    current_directory = os.path.dirname(os.path.abspath(__file__))
    path_to_parquet = os.path.join(current_directory, 'data', 'df_mod_rec_1.parquet')
    df_mod_rec_1 = pq.read_table(path_to_parquet).to_pandas()

    # Configura TF-IDF
    tfidf = TfidfVectorizer(stop_words='english')
    df_mod_rec_1['ntags'] = df_mod_rec_1['ntags'].fillna('')
    tfidf_matrix = tfidf.fit_transform(df_mod_rec_1['ntags'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    indices = pd.Series(df_mod_rec_1.index, index=df_mod_rec_1['app_name']).drop_duplicates()

    try:
        # Índice del juego en la matriz de similitud coseno
        idx = indices[titulo]

        # Puntuaciones para similitud para el juego
        sim_scores = list(enumerate(cosine_sim[idx]))

        # Ordena las puntuaciones de forma descendente
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Índices de los 5 juegos más similares
        game_indices = [i[0] for i in sim_scores[1:6]]

        # Títulos de los 5 juegos más similares
        recommendations = df_mod_rec_1['app_name'].iloc[game_indices].tolist()

        # Devolver las recomendaciones como respuesta JSON
        return JSONResponse(content={"titulo": titulo, "recomendaciones": recommendations})

    except KeyError:
        # Lanzar una excepción HTTP 404 si el juego no se encuentra en el DataFrame
        raise HTTPException(status_code=404, detail=f"El juego '{titulo}' no se encuentra en el DataFrame.")

    

# => ML MODELO DE RECOMENDACION - JUEGOS RECOMENDADOS PARA EL USUARIO
    
@app.get("/recomendacion_usuario/{user_id}")
def get_recomendacion_usuario(user_id: str):

    try:
        # Lee el archivo parquet y obtiene la ruta del directorio actual del script
        current_directory = os.path.dirname(os.path.abspath(__file__))
        path_to_parquet = os.path.join(current_directory, 'data', 'df_mod_rec_2.parquet')
        df_mod_rec_2 = pd.read_parquet(path_to_parquet)

        # Crea una instancia de TfidfVectorizer con stop words 
        tfidf = TfidfVectorizer(stop_words='english')

        # Rellena los valores nulos en la columna 'app_name' con una cadena vacía
        df_mod_rec_2['app_name'] = df_mod_rec_2['app_name'].fillna('')

        # Aplica la transformación TF-IDF a los datos de la columna "app_name"
        tfidf_matrix = tfidf.fit_transform(df_mod_rec_2['app_name'])

        # Entrenar un modelo de clasificación basado en vecinos más cercanos
        X_train, X_test, y_train, y_test = train_test_split(
        tfidf_matrix, df_mod_rec_2['recommend'], test_size=0.2, random_state=42)
        knn_model = KNeighborsClassifier(n_neighbors=5, metric='cosine')
        knn_model.fit(X_train, y_train)

        # Verificar que el ID de usuario sea una cadena válida
        if not isinstance(user_id, str):
            raise HTTPException(status_code=400, detail="El ID de usuario debe ser una cadena")

        # Obtiene el índice del usuario específico en el dataframe
        matching_users = df_mod_rec_2[df_mod_rec_2['user_id'] == user_id]

        if not matching_users.empty:
            user_index = matching_users.index[0]

            # Predecir las recomendaciones usando el modelo entrenado
            _, indices = knn_model.kneighbors(tfidf_matrix[user_index])
            recommendations = df_mod_rec_2['app_name'].iloc[indices.flatten()].tolist()

            # Respuesta en formato JSON
            response_data = {"user_id": user_id, "recomendaciones_de_juegos": recommendations}
            return JSONResponse(content=jsonable_encoder(response_data))
        else:
            return JSONResponse(content=jsonable_encoder({"error": f"No se encontró el usuario con ID: {user_id}"}), status_code=404)
    
    except HTTPException as e:
        # Manejar la excepción y responder con un mensaje de error adecuado
        return JSONResponse(content=jsonable_encoder({"error": str(e)}), status_code=e.status_code)
    except Exception as e:
        # Manejar otras excepciones generales
        return JSONResponse(content=jsonable_encoder({"error": f"Error interno: {str(e)}"}), status_code=500)