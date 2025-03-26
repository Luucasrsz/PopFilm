from __future__ import print_function
from __main__ import app
from flask import request,make_response
import json
import sys
from funciones_auxiliares import Encoder, sanitize_input,delete_session
from controllers import usuarios_controller

@app.route("/api/login",methods=['POST'])
def login():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        login_json = request.json
        if "email" in login_json and "contrasena" in login_json:
            email = sanitize_input(login_json['email'])
            contrasena = sanitize_input(login_json['contrasena'])
            if isinstance(email, str) and isinstance(contrasena, str) and len(email) < 50 and len(contrasena) < 50:
                respuesta,code= usuarios_controller.login(email,contrasena)
            else:
                respuesta={"status":"Bad parameters"}
                code=401
        else:
            respuesta={"status":"Bad request"}
            code=401
    else:
        respuesta={"status":"Bad request"}
        code=401
    response= make_response(json.dumps(respuesta, cls=Encoder), code)
    return response

@app.route("/api/registro",methods=['POST'])
def registro():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        login_json = request.json
        if "usuario" in login_json and "contrasena" in login_json and "perfil" in login_json and "email" in login_json:
            usuario = sanitize_input(login_json['usuario'])
            contrasena = sanitize_input(login_json['contrasena'])
            perfil = sanitize_input(login_json['perfil'])
            email = sanitize_input(login_json['email'])
            if isinstance(usuario, str) and isinstance(contrasena, str) and isinstance(perfil, str) and len(usuario) < 50 and len(contrasena) < 50:
                respuesta,code= usuarios_controller.registro(usuario,contrasena,perfil,email)
            else:
                respuesta={"status":"Bad parameters"}
                code=400
        else:
            respuesta={"status":"Bad request"}
            code=400
    else:
        respuesta={"status":"Bad request"}
        code=400
    response= make_response(json.dumps(respuesta, cls=Encoder), code)
    return response


@app.route("/api/logout",methods=['GET'])
def logout():
    try:
        delete_session()
        ret={"status":"OK"}
        code=200
    except:
        ret={"status":"ERROR"}
        code=500
    response=make_response(json.dumps(ret),code)
    return response
