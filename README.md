[![1.png](https://i.postimg.cc/zGsDyTXW/1.png)](https://postimg.cc/zykYMbhX)

### Proyecto Individual N° 1 (MLOps): Sistema de Recomendación de Videojuegos para Usuarios de Steam

:tw-1f4bd: :tw-1f47e:

#### Descripción

Par este proyecto trabajamos tres arcivos o datas en formato JSON, los cuales presentan una estructura anidada. Se extrae la informacion con el fin de crear un sistema de recomendación. Iniciando desde el tratamiento y recolección de los datos (Data Engineer stuff) hasta el entrenamiento y mantenimiento del modelo de ML según llegan nuevos datos.

##Proceso del Proyecto

**1.- ETL (Extracción, Transformación y Carga)**:

Esta primera etapa se centra en extraer los archivos JSON y convertirlos a archivos CSV. Se realiza la desanidación de las columnas, manteniendo solo aquellas necesarias para el sistema de recomendación y los endpoints propuestos. También se lleva a cabo el tratamiento de valores faltantes con el objetivo de dejar los datos limpios y preparados para su uso en los endpoints y el sistema de recomendación.

El proceso detallado se describe en el proceso de ETL. Como resultado de aplicar el proceso de ETL, se generaron los siguientes archivos CSV: steam_games, user_reviews y user_items.

Cabe destacar que el archivo de user_items se comprimió con la herramienta GZIP debido a limitaciones de espacio.

**2.-Feature Engineering**:

Se ha creado la columna 'sentiment_analysis' aplicando análisis de sentimiento a las reseñas de los usuarios. La asignación de valores es la siguiente: '0' si es una reseña negativa, '1' si es neutral y '2' si es positiva. Esta nueva columna se ha introducido para reemplazar la columna original 'user_reviews.review', facilitando así el trabajo de los modelos de machine learning y el análisis de datos.

**3.- Funciones de consultas**

**`def PlayTimeGenre( genero : str )`**: Debe devolver año con más horas jugadas para dicho género.Notebook
Ejemplo de retorno: {"Año de lanzamiento con más horas jugadas para Género X" : 2013}.

**`def UserForGenre( genero : str )`**: Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.
Ejemplo de retorno: {"Usuario con más horas jugadas para Género X" : us213ndjss09sdf, "Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]}.

**`def UsersRecommend( año : int )`**: Devuelve el top 3 de juegos más recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos/neutrales)
Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}].

**`def UsersWorstDeveloper( año : int )`**: Devuelve el top 3 de desarrolladoras con juegos menos recomendados por usuarios para el año dado. (reviews.recommend = False y comentarios negativos)
Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}].

**`def sentiment_analysis( empresa desarrolladora : str )`**: Según la empresa desarrolladora, se devuelve un diccionario con el nombre de la desarrolladora como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor.
Ejemplo de retorno: {'Valve' : [Negative = 182, Neutral = 120, Positive = 278]}

**4.- API**
Se implementó una API utilizando FastApi para exponer las funciones de consulta como endpoints y tambien se usó Render. El deploy de la API se encuentra en: https://api-steam-games-me3w.onrender.com/docs. El código para la API se encuentra en el archivo main.py.

**5.-EDA**
Durante este proceso, se exploraron y examinaron los conjuntos de datos.

**6.-. Sistema de recomendación**
Crear el sistema de recomendación con dos enfoques distintos:

Sistema de Recomendación ítem-ítem: Modelo que recomienda juegos similares en función de un juego dado. Se utilizó la similitud del coseno como métrica principal para establecer la relación entre juegos.Notebook

Sistema de Recomendación usuario-ítem: Modelo que recomienda juegos a un usuario basándose en las preferencias de otros usuarios similares.Notebook

**7.- Video Explicativo**
Video
