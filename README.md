<p align=center><img src="https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png" height=100><p>

# <h1 align=center> **PROYECTO INDIVIDUAL Nº1** </h1>

# <h1 align=center> ***Autor: Duniet Marrero García*** </h1>

# <h1 align=center>**Tema: Machine Learning Operations (MLOps)**</h1>

<p align="center">
<img src="https://www.crestdatasys.com/wp-content/uploads/elementor/thumbs/chart-02-qccghw7hjmq4y8t66r0vddbb2l07qr6d5k9kgn0c90.jpg"  height=200>
</p>

<p align=center> ¡Este readme corresponde al Proyecto Individual Nro. 1 de la Etapa de labs! para la Cohorte DATA-PT-06.

<hr>  

## **Descripción y Contexto**

Simulando un entorno de trabajo real el proyecto se situa en el estudiante desarrollando un roll de Data Scientist como trabajandor de la  plataforma de distribución digital de videojuegos "Steam".

Steam es un servicio de distribución digital de videojuegos. Fue desarrollado por Valve Corporation y lanzado en septiembre de 2003. Steam está disponible en Microsoft Windows, macOS y otras plataformas.

La emprese solicita crear un modelo de Machine Learning para desarrollar un sistema de recomendación de videojuegos para usuarios.

Para realizar el trabajo se propone el siguiente esquema general:

<p align=center>  <img src="https://scontent.fpss6-1.fna.fbcdn.net/v/t39.30808-6/423247335_7047633531985403_5787616016465433474_n.jpg?_nc_cat=101&ccb=1-7&_nc_sid=3635dc&_nc_eui2=AeGLnT22YXpeTV5qO3cCEyqIfZ0Dx2xS9r99nQPHbFL2vxDMXoyXdGDEi_j9xOvp9gqhsilUVo9lVGMnHuJrXCwJ&_nc_ohc=SAxKJ0Qx8pUAX8YLmBm&_nc_ht=scontent.fpss6-1.fna&oh=00_AfCaCwW2ZImS42Wq9SRbc3sKJiBynITHkISfah1Uwtul2w&oe=65BC79BF"  height=400>
</p>

## **Datasets**

Los tres archivos para iniciar el trabajo se entregaron en formato JSON:

- ***australian_user_reviews.json:*** contiene fundamentalmente los comentarios que los usuarios realizaron sobre los juegos que consumen, recomiendaciones, si el juego es gracioso o no, el id del usuario, la url del perfil y el id del juego.

- ***australian_users_items.json:*** contiene información sobre los juegos que juegan todos los usuarios, así como el tiempo acumulado de horas de juego de cada usuario por los diferentes juegos.

- ***output_steam_games.json:*** contiene los datos relacionados a los juegos en sí, como títulos, generos, desarrolladores, precios, fechas de lanzamientos, especificaciones, etc.

Los Datasets originales (sin procesar) se pueden consultar siguiendo este [Link](https://drive.google.com/drive/folders/1k_f3odHUPy3nQOt9qzOuMQnDcNpsX2En?usp=sharing).

## **Análisis Exploratorio de los Datos (EDA)**

Los datasets de trabajo se entregaron por parte de la empresa en formato .JSON con columnas de datos anidados, razón por la cual se procesaron utilizando la función "normalize"  para aplanar las columnas y obtener los datos en el formato adecuado.

El EDA realizado se puede consultar en el siguiente [notebook](https://colab.research.google.com/drive/1KFP8n18x3_jHysXZkNCAxP8-r6BTAo3p?usp=sharing) de Google Colaboratory.


## **Extracción, Transformación y Carga de los datos (ETL)**

Se realizaron las transformaciones de los datos para leer el dataset con en el formato y tipo de datos correctos. Se eliminaron o imputaron datos nulos, se eliminaron duplicados y columnas que no se necesitan para responder las consultas o preparar los modelos de aprendizaje automático, de esta forma se pudo optimizar el rendimiento de la API. Finalmente estos archivos se exportaron y guardaron en formato CSV.

El proceso de ETL se puede consultar en el siguiente [notebook](https://colab.research.google.com/drive/1gRGEWNJTvKI-PIOo9EgD6j9HVNSzHmOT?usp=sharing) de Google Colaboratory.

Los archivos resultantes luego del proceso de ETL se pueden consultar siguiendo este [Link](https://drive.google.com/drive/folders/1jJBJH0Zm1ynoFom9Azflzr7ENGKMjh-K?usp=sharing)

## **Feature Engineering**

Se aplicó un "análisis de sentimiento" a las reseñas (reviews) de los usuarios clasificandolos segun la siguiente escala:

- Valor 0: negativo
- Valor 1: neutral o sin review
- Valor 2: positivo.

El análisis se realizó utilizando la librería TextBlob de procesamiento de lenguaje natural (NLP) en Phyton, la cual calcula calcular la polaridad de sentimiento y los datos resultantes se almacenaron en una nueva columna llamada 'sentiment_analysis' que reemplazó a la columna 'reviews'.

El Procesamiento de Lenguaje Natural (NLP) realizado se puede consultar en el siguiente [notebook](https://colab.research.google.com/drive/1KKGA4sccL7xBIOV4OcsLZQstLWcQABDN?usp=sharing) de Google Colaboratory.


## **Desarrollo de la API**

En este proyecto se utilizó **FastAPI**, la cual tiene la ventaja de simplificar el desarrollo de APIs en Python y proporciona herramientas poderosas y eficientes y es de código abierto. FastAPI además genera automáticamente documentación interactiva para la API a partir de las anotaciones de tipo y los comentarios en el código. La documentación puede consultarse en el siguiente [Link](https://deploy-api-proy-int-1-duniet-marrero.onrender.com) 

Las consultas que se pueden realizar desde la API son las siguientes:

+ def **developer (desarrollador : str )**: A parir de un input "desarrollador de juegos" devuelve la cantidad de items y porcentaje de contenido Free por año para la empresa desarrolladora. 

+ def **userdata (User_id : str )**: Utilizando un User_id como input, retorna la cantidad de dinero gastado por el usuario, el porcentaje de recomendación en base a reviews.recommend y la cantidad de items.

+ def **UserForGenre (genero : str)**: Para un genero dado (input) devuelve el usuario que acumula más horas jugadas y una lista de la acumulación de horas jugadas por año de lanzamiento.

+ def **best_developer_year (año` : int)**: Devuelve el "Top 3" de desarrolladores con juegos más recomendados por usuarios para el año dado (input). El análisis de reviews.recommend considera las condiciones de recomended con valor True y comentarios positivos y neutrales.
  
+ def **developer_reviews_analysis (desarrolladora : str)**: Según el desarrollador (input), devuelve la cantidad total de registros de reseñas de usuarios categorizadas con un análisis de sentimiento como valor positivo y negativo. 

## **Análisis exploratorio de los datos (EDA)**

Una vez analizados y transformados los datos primarios realizando las tareas de limpieza necesarias, se procede a analizar las relaciones que hay entre las variables del dataset, (outliers o anomalías, patrones, correlaciones entre variables, analisis de reviews, etc.) A partir de este análisis se procedió a realizar los modelos de recomendación. 

## **Modelos de Recomendación (ML)**

+ def **recomendacion_juego (id de producto)**: Ingresando el id de producto (input), devuelve una lista con 5 juegos recomendados similares al ingresado.

+ def **recomendacion_usuario (id de usuario)**: Ingresando el id de un usuario (input), retorna una lista con 5 juegos recomendados para dicho usuario.

Los detalles de los modelos de recomendación se pueden consultar en el siguiente [notebook](https://colab.research.google.com/drive/1KKGA4sccL7xBIOV4OcsLZQstLWcQABDN?usp=sharing) de Google Colaboratory.


## **Video** 

Finalmente se incluye un video explicativo mostrando el proceso de desarrollo del proyecto y el resultado de las consultas propuestas y del modelo de Machine Learning, al mismo puede accederse desde este [Link]().

<br/>

