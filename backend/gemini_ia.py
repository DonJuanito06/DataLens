import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Cargar la configuración desde el archivo .env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# 2. Configurar la API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 3. Definir el modelo que ya comprobamos que funciona
model = genai.GenerativeModel('gemini-flash-latest')

def analizar_datos_con_ia(prompt):
    """
    Envía el texto procesado del Excel a Gemini y devuelve el análisis.
    """
    try:
        # Petición directa al modelo funcional
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Solo capturamos errores reales de conexión o de la API
        return f"Error técnico al conectar con la IA: {str(e)}"