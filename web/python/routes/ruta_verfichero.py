from __future__ import print_function
from __main__ import app
from flask import request, jsonify
import os
import json

@app.route('/api/ver/<archivo>', methods=['GET'])
def ver(archivo):
    try:
        # Sanitizar el nombre del archivo para evitar rutas o comandos maliciosos
        archivo = os.path.basename(archivo)  # Evita rutas relativas como '../etc/passwd'
        
        # Definir la ruta base de los archivos que se pueden leer
        basepath = os.path.dirname(__file__)
        upload_path = os.path.join(basepath, 'static', archivo)

        # Verificar si el archivo existe dentro de la carpeta 'static'
        if not os.path.exists(upload_path):
            return jsonify({"status": "ERROR", "mensaje": "El archivo no existe"}), 404

        # Verificar que el archivo sea un archivo normal (no un directorio)
        if not os.path.isfile(upload_path):
            return jsonify({"status": "ERROR", "mensaje": "No es un archivo válido"}), 400

        # Leer el contenido del archivo de manera segura
        with open(upload_path, 'r', encoding='utf-8') as file:
            contenido = file.read()

        return jsonify({"status": "OK", "contenido": contenido}), 200

    except Exception as e:
        # Manejo de errores genérico con el mensaje del error
        return jsonify({"status": "ERROR", "mensaje": str(e)}), 500
