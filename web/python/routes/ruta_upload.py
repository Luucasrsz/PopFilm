from __future__ import print_function
from __main__ import app
from flask import request
import os
import json
import sys

@app.route('/api/upload', methods=['POST'])
def upload():
    try:
        f = request.files['fichero']  # Obtener el archivo
        user_input = request.form.get("nombre")  # Obtener el nombre de la película
        basepath = os.path.dirname(__file__)  # Ruta del archivo actual
        upload_path = os.path.join(basepath, 'static', user_input)  # Ruta de destino para el archivo

        print('Lugar de guardado: ' + upload_path, file=sys.stdout)

        # Verificar que la carpeta exista, si no, crearla
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
        
        # Guardar el archivo en la ruta indicada
        f.save(upload_path)
        return json.dumps({"status": "OK"}), 200
    except Exception as e:
        print(f"Error al subir el archivo: {e}", file=sys.stdout)
        return json.dumps({"status": "ERROR"}), 500
