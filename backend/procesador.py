import pandas as pd
import io

def procesar_excel_albergue(archivo_storage):
    """
    Lee el archivo Excel y lo convierte en texto para la IA.
    """
    try:
        # Leemos el archivo desde la memoria
        df = pd.read_excel(archivo_storage)
        
        # Limpiamos nombres de columnas (quitar espacios)
        df.columns = [str(c).strip() for c in df.columns]
        
        # Convertimos a JSON para el frontend (primeras 10 filas para no saturar)
        datos_json = df.head(10).to_dict(orient='records')
        
        # Creamos un resumen en texto para que Gemini lo lea fácil
        # Solo tomamos las columnas más importantes para ahorrar tokens
        resumen_texto = df.to_string(index=False)
        
        return datos_json, resumen_texto
        
    except Exception as e:
        raise Exception(f"Error al procesar el Excel: {str(e)}")