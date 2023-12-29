from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import scipy as sp
import operator


app = FastAPI(title='API Steam Games')

#Mensaje de bienvenida
@app.get("/")
async def root():
    return {"Mensaje": "Bienvenidos a mi proyecto"}


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
            anio_mas_jugado = df_genero.loc[df_genero['playtime_forever'].idxmax()]['release_year']
            
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