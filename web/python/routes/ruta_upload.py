from __future__ import print_function
from flask import Flask, request, jsonify, make_response
from __main__ import app
import os
import json
import sys
from funciones_auxiliares import sanitize_input


@app.route ('/upload', methods=['POST']) 
def upload():
    try:
        if (validar_session_normal()):
            f= request.files['fichero'] 
            user_input = request.form.get("nombre")
            basepath = os.path.dirname(__file__) # ruta del archivo actual
            upload_path = os.path.join (basepath,'static',user_input) 
            print('lugar' +  upload_path, file=sys.stdout)
            f.save(upload_path)
            respuesta={"status": "OK"}
            code=200
        else:
            respuesta={"status":"Forbidden"}
            code=403
    except:
        respuesta={"status": "ERROR"}
        code=500
    response=make_response(json.dumps(respuesta),code)
    return response