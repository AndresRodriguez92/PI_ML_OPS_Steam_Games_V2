from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import scipy as sp
import operator


app = FastAPI(title='API Steam Games')

#Mensaje de bienvenida
@app.get("/")
async def root():
    return {"Mensaje": "Bienvenidos a mi proyecto Individual"}


#PlayTimeGenre
@app.get("/PlayTimeGenre/{genero :str}")
async def user(genero: str):
    """
    Obtiene el año de lanzamiento con más horas jugadas
    para un género de juegos específico.

    Parámetros:
        genero (str): El género de juegos para el cual se quiere obtener la información.

    Returns:
        JSONResponse: Una respuesta JSON con el año de lanzamiento con más horas jugadas
        para el género especificado, ó un mensaje de error si no se encuentra información.
    """
    try:
        # Cargar el DataFrame desde el archivo CSV
        df_genero = pd.read_csv(r"C:\Users\ayrc2\Documentos\Proyecto Individual DPT03\PI_ML_OPS_Steam_Games_V2\Data\PlayTimeGenre.csv")

        # Filtrar el DataFrame para obtener solo las filas del género especificado
        df_genero = df_genero[df_genero['genres'] == genero]

        if not df_genero.empty:
            # Encontrar el año con la máxima cantidad de horas jugadas
            anio_mas_jugado = df_genero.loc[df_genero['playtime_forever'].idxmax()]['Año_estreno']
            
            # Crear y devolver una respuesta exitosa
            return JSONResponse(
                status_code=200,
                content={
                    "results": f'Año de lanzamiento con más horas jugadas para el género {genero}: {int(anio_mas_jugado)}'
                }
            )
        else:
            # Devolver una respuesta de error si no se encuentra información para el género
            return JSONResponse(
                status_code=404,
                content={'error': f"No se encontró información del género '{genero}'"}
            )

    except Exception as e:
        # Manejar cualquier excepción y devolver una respuesta de error
        return JSONResponse(
            status_code=500,
            content={'error': f"Error interno: {str(e)}"}
        )
    
    
#UserForGenre
@app.get("/UserForGenre/{genero :str}")
async def user(genero: str):
    """
    Obtiene el usuario con el mayor tiempo de juego para un género dado.

    Parámetros:
    - genero: El género para el cual se solicita la información del usuario.

    Devuelve:
    - Respuesta JSON que contiene al usuario con mayor tiempo de juego para el género especificado y su tiempo de juego por año.
    """
    try:
        # Leer el archivo CSV que contiene la información del usuario para el género dado
        df_usuario_por_genero = pd.read_csv(r"C:\Users\ayrc2\Documentos\Proyecto Individual DPT03\PI_ML_OPS_Steam_Games_V2\Data\UserForGenre.csv")

        # Filtrar datos para el género especificado
        datos_genero = df_usuario_por_genero[df_usuario_por_genero['genres'] == genero]

        if not datos_genero.empty:
            # Crear una lista de diccionarios para el tiempo de juego por año
            tiempo_juego_por_anio = [{'Año': anio, 'Tiempo de Juego': tiempo_juego} for anio, tiempo_juego in datos_genero[['Año_estreno', 'playtime_forever']].values]

            # Crear el diccionario de salida
            resultado = {
                'Usuario con mayor tiempo de juego para el género ' + genero: datos_genero.iloc[0]['user_id'],
                'Horas jugadas': tiempo_juego_por_anio
            }

            return resultado
        else:
            # Devolver una respuesta de error si no se encuentra información para el género
            return JSONResponse(
                status_code=404,
                content={'error': f"No se encontró información del género '{genero}'"}
            )

    except Exception as e:
        # Manejar cualquier excepción y devolver una respuesta 500
        raise HTTPException(
            status_code=500,
            detail=f"Error Interno del Servidor: {str(e)}"
        )
    

#UsersRecommend
@app.get("/UsersRecommend/{año :int}")
async def user(año: int):
    """
    Obtiene los 3 juegos más recomendados por usuarios para el año ingresado.

    Parámetros:
    - año (int): El año para el cual se desean obtener las recomendaciones.

    Returns:
    - dict: Un diccionario que contiene el top 3 de juegos recomendados en el formato:
        {"Puesto 1": "Nombre del Juego1", "Puesto 2": "Nombre del Juego2", "Puesto 3": "Nombre del Juego3"}
        En caso de no haber recomendaciones para el año especificado, devuelve una respuesta de error.
    """
    try:
        # Leer el archivo CSV que contiene la información de las recomendaciones para el año dado
        recomendaciones_anio = pd.read_csv(r"C:\Users\ayrc2\Documentos\Proyecto Individual DPT03\PI_ML_OPS_Steam_Games_V2\Data\UsersRecommend.csv")

        # Verificar si hay revisiones para el año dado
        if not recomendaciones_anio.empty:
            # Filtrar las revisiones para el año dado y recomendaciones positivas/neutrales
            recomendaciones = recomendaciones_anio[recomendaciones_anio['posted_year'] == int(año)]
            
            # Ordenar en orden descendente por la cantidad de recomendaciones
            recomendaciones = recomendaciones.sort_values('recommend', ascending=False)
            
            # Crear una única línea de resultado
            resultado = {
                "Puesto 1": recomendaciones.iloc[0]['app_name'],
                "Puesto 2": recomendaciones.iloc[1]['app_name'],
                "Puesto 3": recomendaciones.iloc[2]['app_name']
            }
            
            return resultado
        else:
            # Devolver una respuesta de error si no se encuentra información para el año
            return JSONResponse(
                status_code=404,
                content={'error': f"No hay recomendaciones para el año {año}"}
            )
    except Exception as e:
        # Manejar cualquier excepción y devolver una respuesta 500
        raise HTTPException(
            status_code=500,
            detail=f"Error Interno del Servidor: {str(e)}"
        )
    

#UsersNotRecommend
@app.get("/UsersNotRecommend/{año :int}")
async def user(año: int):
    """
    Obtiene los 3 juegos Menos recomendados por usuarios para el año ingresado.

    Parámetros:
    - año (int): El año para el cual se desean obtener las recomendaciones.

    Returns:
    - dict: Un diccionario que contiene el top 3 de juegos Menos recomendados en el formato:
        {"Puesto 1": "Nombre del Juego1", "Puesto 2": "Nombre del Juego2", "Puesto 3": "Nombre del Juego3"}
        En caso de no haber recomendaciones para el año especificado, devuelve una respuesta de error.
    """
    try:
        # Leer el archivo CSV que contiene la información de las recomendaciones para el año dado
        recomendaciones_anio_2 = pd.read_csv(r"C:\Users\ayrc2\Documentos\Proyecto Individual DPT03\PI_ML_OPS_Steam_Games_V2\Data\UsersNotRecommend.csv")

        # Verificar si hay revisiones para el año dado
        if not recomendaciones_anio_2.empty:
            # Filtrar las revisiones para el año dado y recomendaciones positivas/neutrales
            recomendaciones_2 = recomendaciones_anio_2[recomendaciones_anio_2['posted_year'] == int(año)]
            
            # Ordenar en orden descendente por la cantidad de recomendaciones
            recomendaciones_2 = recomendaciones_2.sort_values('recommend', ascending=False)
            
            # Crear una única línea de resultado
            resultado = {
                "Puesto 1": recomendaciones_2.iloc[0]['app_name'],
                "Puesto 2": recomendaciones_2.iloc[1]['app_name'],
                "Puesto 3": recomendaciones_2.iloc[2]['app_name']
            }
            
            return resultado
        else:
            # Devolver una respuesta de error si no se encuentra información para el año
            return JSONResponse(
                status_code=404,
                content={'error': f"No hay recomendaciones para el año {año}"}
            )
    except Exception as e:
        # Manejar cualquier excepción y devolver una respuesta 500
        raise HTTPException(
            status_code=500,
            detail=f"Error Interno del Servidor: {str(e)}"
        )
    

#sentiment_analysis
@app.get("/sentimet_analysis/{anio}", name = "SENTIMENT_ANALYSIS")
async def sentiment_analysis(anio):

    """
    La siguiente función retorna el resultado de los analisis de sentimiento por año ingresado, 
    se tiene en cuenta el año de estreno del juego.
    
    Paramentros: 
    
            - anio (int): Año de estreno del juego
    Retorna:
    
            - count_sentiment : una lista del conteo de sentimientos
    Ejemplo:
    
            -anio: 2015
    """
    # Leer el archivo CSV que contiene la información de las recomendaciones para el año dado
    sentimiento_analysis = pd.read_csv(r"C:\Users\ayrc2\Documentos\Proyecto Individual DPT03\PI_ML_OPS_Steam_Games_V2\Data\sentimiento_analysis.csv")
    
    #Se filtran las reviews por año y las igualo al año que se ingresa en la consulta transformandolo en string 
    reviews_por_anio= sentimiento_analysis[sentimiento_analysis["release_anio"]== str(anio)]
    
    #Se inicia una lista vacia por cada sentimiento para ir contandolos 
    Negativos = 0
    Neutral = 0
    Positivos = 0
    
    #Se itera sobre las filas de reviews_por_anio y se distibuyen los datos segun la columna "sentiment_analysis"
    for i in reviews_por_anio["sentiment_analisis"]:
        if i == 0:
            Negativos += 1
        elif i == 1:
            Neutral += 1 
        elif i == 2:
            Positivos += 1

    count_sentiment ={"Negative": Negativos , "Neutral" : Neutral, "Positive": Positivos}
    
    return count_sentiment


#Modelo de recomendacion item_item
@app.get("/recomendacion_juego/{id}", name= "RECOMENDACION_JUEGO")
async def recomendacion_juego(id: int):
    
    """La siguiente funcion genera una lista de 5 juegos similares a un juego dado (id)
    
    Parametros:
    
        -id (int): El id del juego para el que se desean encontrar juegos similares

    Returna:
    
        -dict Un diccionario con 5 juegos similares 
    """
    modelo_render = pd.read_csv(r"C:\Users\ayrc2\Documentos\Proyecto Individual DPT03\PI_ML_OPS_Steam_Games_V2\Data\modelo_render.csv")
    
    game = modelo_render[modelo_render['id'] == id]

    if game.empty:
        return("El juego '{id}' no posee registros.")
    
    # Obtiene el índice del juego dado
    idx = game.index[0]

    # Toma una muestra aleatoria del DataFrame df_games
    sample_size = 2000  # Define el tamaño de la muestra (ajusta según sea necesario)
    df_sample = modelo_render.sample(n=sample_size, random_state=42)  # Ajusta la semilla aleatoria según sea necesario

    # Calcula la similitud de contenido solo para el juego dado y la muestra
    sim_scores = cosine_similarity([modelo_render.iloc[idx, 3:]], df_sample.iloc[:, 3:])

    # Obtiene las puntuaciones de similitud del juego dado con otros juegos
    sim_scores = sim_scores[0]

    # Ordena los juegos por similitud en orden descendente
    similar_games = [(i, sim_scores[i]) for i in range(len(sim_scores)) if i != idx]
    similar_games = sorted(similar_games, key=lambda x: x[1], reverse=True)

    # Obtiene los 5 juegos más similares
    similar_game_indices = [i[0] for i in similar_games[:5]]

    # Lista de juegos similares (solo nombres)
    similar_game_names = df_sample['app_name'].iloc[similar_game_indices].tolist()

    return {"similar_games": similar_game_names}