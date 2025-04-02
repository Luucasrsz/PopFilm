from __future__ import print_function
from __main__ import app
from flask import request, jsonify
from funciones_auxiliares import validar_session_normal
import os
import sys
import json
import subprocess

@app.route('/api/ver/<archivo>', methods=['GET'])
def ver(archivo):
    try:
        if (validar_session_normal()):
            basepath = os.path.dirname(__file__) # ruta del archivo actual
            upload_path = os.path.join (basepath,'static',archivo) 
            #if os.path.exists(upload_path):
            salida=subprocess.getoutput("cat " + upload_path)
            respuesta={"status":"OK", "contenido": salida}
            code=200
        else:
            respuesta={"status":"Forbidden"}
            code=403
    except:
        respuesta= {"status": "ERROR"}
        code=500
    response=make_response(json.dumps(respuesta),code)
    return response
