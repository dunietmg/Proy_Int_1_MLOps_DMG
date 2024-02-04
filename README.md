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

Simulando un entorno de trabajo real el proyecto se situa en el estudiante desarrollando un roll de **`Data Scientist`** como trabajandor de la  plataforma de distribución digital de videojuegos "Steam".

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



**`Desarrollo API`**:   Propones disponibilizar los datos de la empresa usando el framework ***FastAPI***. Las consultas que propones son las siguientes:

<sub> Debes crear las siguientes funciones para los endpoints que se consumirán en la API, recuerden que deben tener un decorador por cada una (@app.get(‘/’)).<sub/>


+ def **developer( *`desarrollador` : str* )**:
    `Cantidad` de items y `porcentaje` de contenido Free por año según empresa desarrolladora. 
Ejemplo de retorno:

| Año  | Cantidad de Items | Contenido Free  |
|------|-------------------|------------------|
| 2023 | 50                | 27%              |
| 2022 | 45                | 25%              |
| xxxx | xx                | xx%              |


+ def **userdata( *`User_id` : str* )**:
    Debe devolver `cantidad` de dinero gastado por el usuario, el `porcentaje` de recomendación en base a reviews.recommend y `cantidad de items`.

Ejemplo de retorno: {"Usuario X" : us213ndjss09sdf, "Dinero gastado": 200 USD, "% de recomendación": 20%, "cantidad de items": 5}

+ def **UserForGenre( *`genero` : str* )**:
    Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año de lanzamiento.

Ejemplo de retorno: {"Usuario con más horas jugadas para Género X" : us213ndjss09sdf,
			     "Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]}
	
+ def **best_developer_year( *`año` : int* )**:
   Devuelve el top 3 de desarrolladores con juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos)
  
Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]

+ def **developer_reviews_analysis( *`desarrolladora` : str* )**:
    Según el desarrollador, se devuelve un diccionario con el nombre del desarrollador como llave y una lista con la cantidad total 
    de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor positivo o negativo. 

Ejemplo de retorno: {'Valve' : [Negative = 182, Positive = 278]}

<br/>

> `Importante`<br>
El MVP _tiene_ que ser una API que pueda ser consumida segun los criterios de [API REST o RESTful](https://rockcontent.com/es/blog/api-rest/) desde cualquier dispositivo conectado a internet. Algunas herramientas como por ejemplo, Streamlit, si bien pueden brindar una interfaz de consulta, no cumplen con las condiciones para ser consideradas una API, sin workarounds.


**`Deployment`**: Conoces sobre [Render](https://render.com/docs/free#free-web-services) y tienes un [tutorial de Render](https://github.com/HX-FNegrete/render-fastapi-tutorial) que te hace la vida mas fácil :smile: . También podrías usar [Railway](https://railway.app/), o cualquier otro servicio que permita que la API pueda ser consumida desde la web.

<br/>

**`Análisis exploratorio de los datos`**: _(Exploratory Data Analysis-EDA)_

Ya los datos están limpios, ahora es tiempo de investigar las relaciones que hay entre las variables del dataset, ver si hay outliers o anomalías (que no tienen que ser errores necesariamente :eyes: ), y ver si hay algún patrón interesante que valga la pena explorar en un análisis posterior. Las nubes de palabras dan una buena idea de cuáles palabras son más frecuentes en los títulos, ¡podría ayudar al sistema de predicción! En esta ocasión vamos a pedirte que no uses librerías para hacer EDA automático ya que queremos que pongas en práctica los conceptos y tareas involucrados en el mismo. Puedes leer un poco más sobre EDA en [este articulo](https://medium.com/swlh/introduction-to-exploratory-data-analysis-eda-d83424e47151)

**`Modelo de aprendizaje automático`**: 

Una vez que toda la data es consumible por la API, está lista para consumir por los departamentos de Analytics y Machine Learning, y nuestro EDA nos permite entender bien los datos a los que tenemos acceso, es hora de entrenar nuestro modelo de machine learning para armar un **sistema de recomendación**. Para ello, te ofrecen dos propuestas de trabajo: En la primera, el modelo deberá tener una relación ítem-ítem, esto es se toma un item, en base a que tan similar esa ese ítem al resto, se recomiendan similares. Aquí el input es un juego y el output es una lista de juegos recomendados, para ello recomendamos aplicar la *similitud del coseno*. 
La otra propuesta para el sistema de recomendación debe aplicar el filtro user-item, esto es tomar un usuario, se encuentran usuarios similares y se recomiendan ítems que a esos usuarios similares les gustaron. En este caso el input es un usuario y el output es una lista de juegos que se le recomienda a ese usuario, en general se explican como “A usuarios que son similares a tí también les gustó…”. 
Deben crear al menos **uno** de los dos sistemas de recomendación (Si se atreven a tomar el desafío, para mostrar su capacidad al equipo, ¡pueden hacer ambos!). Tu líder pide que el modelo derive obligatoriamente en un GET/POST en la API símil al siguiente formato:

Si es un sistema de recomendación item-item:
+ def **recomendacion_juego( *`id de producto`* )**:
    Ingresando el id de producto, deberíamos recibir una lista con 5 juegos recomendados similares al ingresado.

Si es un sistema de recomendación user-item:
+ def **recomendacion_usuario( *`id de usuario`* )**:
    Ingresando el id de un usuario, deberíamos recibir una lista con 5 juegos recomendados para dicho usuario.


**`Video`**: Necesitas que al equipo le quede claro que tus herramientas funcionan realmente! Haces un video mostrando el resultado de las consultas propuestas y de tu modelo de ML entrenado! Recuerda presentarte, contar muy brevemente de que trata el proyecto y lo que vas a estar mostrando en el video.
Para grabarlo, puedes usar la herramienta Zoom, haciendo una videollamada y grabando la pantalla, aunque seguramente buscando, encuentres muchas formas más. 😉

<sub> **Spoiler**: El video NO DEBE durar mas de ***7 minutos*** y DEBE mostrar las consultas requeridas en funcionamiento desde la API y una breve explicación del modelo utilizado para el sistema de recomendación. En caso de que te sobre tiempo luego de grabarlo, puedes mostrar/explicar tu EDA, ETL e incluso cómo desarrollaste la API. <sub/>

<br/>

## **Criterios de evaluación**

**`Código`**: Prolijidad de código, uso de clases y/o funciones, en caso de ser necesario, código comentado. Se tendrá en cuenta el trato de los valores str como `COUNter-strike` / `COUNTER-STRIKE` / `counter-strike`.

**`Repositorio`**: Nombres de archivo adecuados, uso de carpetas para ordenar los archivos, README.md presentando el proyecto y el trabajo realizado. Recuerda que este último corresponde a la guía de tu proyecto, no importa que tan corto/largo sea siempre y cuando tu 'yo' + 1.5 AÑOS pueda entenderlo con facilidad. 

**`Cumplimiento`** de los requerimientos de aprobación indicados en el apartado `Propuesta de trabajo`

NOTA: Recuerde entregar el link de acceso al video. Puede alojarse en YouTube, Drive o cualquier plataforma de almacenamiento. **Verificar que sea de acceso público, recomendamos usar modo incógnito en tu navegador para confirmarlo**.

<br/>
Aquí te sintetizamos que es lo que consideramos un MVP aprobatorio, y la diferencia con un producto completo.



<p align="center">
<img src="https://github.com/HX-PRomero/PI_ML_OPS/raw/main/src/MVP_MLops.PNG"  height=250>
</p>


## **Fuente de datos**

+ [Dataset](https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj): Carpeta con el archivo que requieren ser procesados, tengan en cuenta que hay datos que estan anidados (un diccionario o una lista como valores en la fila).
+ [Diccionario de datos](https://docs.google.com/spreadsheets/d/1-t9HLzLHIGXvliq56UE_gMaWBVTPfrlTf2D9uAtLGrk/edit?usp=drive_link): Diccionario con algunas descripciones de las columnas disponibles en el dataset.
<br/>

## **Material de apoyo**

En este mismo repositorio podrás encontrar algunos (hay repositorios con distintos sistemas de recomendación) [links de ayuda](https://github.com/HX-PRomero/PI_ML_OPS/raw/main/Material%20de%20apoyo.md). Recuerda que no son los unicos recursos que puedes utilizar!


