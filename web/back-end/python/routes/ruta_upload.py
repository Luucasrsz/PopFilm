from __future__ import print_function
from __main__ import app
from flask import request
import os
import json
import sys

@app.route ('/upload', methods=['POST']) 
def upload():
    try:
        f= request.files['fichero']
        user_input = request.form.get("nombre")
        basepath = os.path.dirname(__file__) # ruta del archivo actual
        upload_path = os.path.join (basepath,'static',user_input) 
        print('lugar' +  upload_path, file=sys.stdout)
        f.save(upload_path)
        return json.dumps({"status": "OK"}),200
    except:
        return json.dumps({"status": "ERROR"}), 500