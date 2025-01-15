from __future__ import print_function
from __main__ import app
from flask import request
import os
import sys
import json
import subprocess

@app.route ('/ver/<archivo>', methods=['GET']) 
def ver(archivo):
    try:    
        basepath = os.path.dirname(__file__) # ruta del archivo actual
        upload_path = os.path.join (basepath,'static',archivo) 
        #if os.path.exists(upload_path):
        salida=subprocess.getoutput("cat " + upload_path)
        return json.dumps({"status":"OK", "contenido": salida}),200
        #else:
        #    return json.dumps({"status":"ERROR", "mensaje": "El archivo no existe"}),200
    except:
        return json.dumps({"status": "ERROR"}), 500