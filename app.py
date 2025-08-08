from flask import Flask, jsonify, render_template
import pandas as pd
import os

# Inicializar la aplicación Flask
app = Flask(__name__)

# --- Rutas de la API ---

@app.route('/api/recintos')
def get_recintos():
    """
    Endpoint de la API para obtener los datos de los recintos.
    Lee el archivo CSV y lo devuelve en formato JSON.
    """
    try:
        # La ruta al archivo CSV. Debe estar en la misma carpeta que app.py
        csv_path = 'GeoRecintos_Scz.xlsx - Hoja1.csv'
        if not os.path.exists(csv_path):
            return jsonify({"error": "El archivo CSV no se encontró en el servidor."}), 404

        # --- CORRECCIÓN IMPORTANTE ---
        # Leer los datos usando pandas, especificando el encoding a UTF-8.
        # Esto asegura que los caracteres especiales se lean correctamente.
        df = pd.read_csv(csv_path, encoding='utf-8')

        # Limpia los espacios en blanco al inicio y final de los nombres de las columnas.
        df.columns = df.columns.str.strip()

        # Filtrar filas que no tengan latitud o longitud
        df.dropna(subset=['latitud', 'longitud'], inplace=True)
        
        # Reemplazar los valores NaN (Not a Number) de pandas por None (null en JSON).
        df = df.astype(object).where(pd.notnull(df), None)
        
        # Convertir el DataFrame a una lista de diccionarios (JSON)
        recintos_data = df.to_dict(orient='records')
        
        return jsonify(recintos_data)

    except Exception as e:
        # Manejo de errores por si el archivo CSV está corrupto o hay otros problemas
        return jsonify({"error": str(e)}), 500

# --- Ruta para servir la página principal ---

@app.route('/')
def index():
    """
    Sirve el archivo principal de la aplicación (index.html).
    Flask buscará este archivo en una carpeta llamada 'templates'.
    """
    return render_template('index.html')

# --- Iniciar el servidor ---

if __name__ == '__main__':
    # Ejecuta la aplicación en modo de depuración para facilitar el desarrollo
    app.run(debug=True)
    
    app.run(debug=True)
