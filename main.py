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
        df_genero = pd.read_csv(r"C:\Users\ayrc2\Documentos\Proyecto Individual DPT03\PI_ML_OPS_Steam_Games_V2\PI_ML_OPS_Steam_Games_V2\Data\PlayTimeGenre.csv")

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
        df_usuario_por_genero = pd.read_csv(r"C:\Users\ayrc2\Documentos\Proyecto Individual DPT03\PI_ML_OPS_Steam_Games_V2\PI_ML_OPS_Steam_Games_V2\Data\UserForGenre.csv")

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