from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from procesador import procesar_excel_albergue
from gemini_ia import analizar_datos_con_ia

app = Flask(__name__)
CORS(app) 

@app.route('/analizar', methods=['POST'])
def analizar():
    if 'file' not in request.files:
        return jsonify({"error": "No se subió ningún archivo"}), 400
    
    archivo = request.files['file']
    # Recibimos el contexto (poblacional o financiero) desde el frontend
    contexto = request.form.get('contexto', 'poblacional')
    
    try:
        # 1. Extraemos los datos del Excel
        datos_json, resumen_texto = procesar_excel_albergue(archivo)
        
        # 2. Personalizamos el prompt según el botón presionado
        if contexto == "financiero":
            instruccion = f"""
            Actúa como un experto en FINANZAS y ECONOMÍA SOCIAL.
            Analiza estos datos: {resumen_texto}
            
            REGLAS:
            1. Enfócate SOLO en necesidades financieras, empleabilidad y riesgos económicos.
            2. NO incluyas análisis demográfico detallado.
            3. NO USES FORMATO MARKDOWN (sin asteriscos **, sin almohadillas #, sin símbolos raros).
            4. Escribe títulos en MAYÚSCULAS y usa párrafos limpios.
            """
        else:
            instruccion = f"""
            Actúa como un experto en SOCIOLOGÍA y DEMOGRAFÍA.
            Analiza estos datos: {resumen_texto}
            
            REGLAS:
            1. Enfócate SOLO en la población (edades, géneros, nacionalidades y casos sociales).
            2. NO incluyas análisis financiero ni de costos.
            3. NO USES FORMATO MARKDOWN (sin asteriscos **, sin almohadillas #, sin símbolos raros).
            4. Escribe títulos en MAYÚSCULAS y usa párrafos limpios.
            """
        
        # 3. Llamamos a Gemini con la instrucción específica
        analisis = analizar_datos_con_ia(instruccion)
        
        return jsonify({
            "status": "success",
            "data": datos_json,
            "analysis": analisis
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Azure asigna el puerto automáticamente, por eso usamos os.environ.get
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)