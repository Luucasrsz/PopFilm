from flask import request, jsonify, make_response
import os
import decimal
import json
from __main__ import app
from controllers import peliculas_controller
from funciones_auxiliares import sanitize_input, Encoder, prepare_response_extra_headers, validar_session_normal, validar_session_admin

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super().default(obj)

@app.route("/api/peliculas", methods=["GET"])
def peliculas():
    if (validar_session_normal()):
        respuesta, code = peliculas_controller.obtener_peliculas()
    else:
        respuesta={"status":"Forbidden"}
        code=403
    response= make_response(json.dumps(respuesta, cls=Encoder), code)
    return response

@app.route("/api/pelicula/<id>", methods=["GET"])
def pelicula_por_id(id):
    id = sanitize_input(id)
    if isinstance(id, str) and len(id)<64:
        if (validar_session_normal()):
            respuesta, code = peliculas_controller.obtener_pelicula_por_id(id)
        else:
            respuesta={"status":"Bad parameters"}
            code=403 
    
    response= make_response(json.dumps(respuesta, cls=Encoder), code)
    return response

@app.route("/api/peliculas/insertar", methods=["POST"])
def guardar_pelicula():
    content_type = request.headers.get('Content-Type')
    
    if (content_type == 'application/json'):
        pelicula_json = request.json
        if "nombre" in pelicula_json and "sinopsis" in pelicula_json and "categoria" in pelicula_json and "precio" in pelicula_json:
            nombre = sanitize_input(pelicula_json["nombre"])
            sinopsis = sanitize_input(pelicula_json["sinopsis"])
            precio = pelicula_json["precio"]
            categoria = sanitize_input(pelicula_json["categoria"])
         
            if isinstance(nombre, str) and isinstance(sinopsis, str) and isinstance(categoria, str) and len(nombre)<128 and len(sinopsis)<512 and len(categoria)<512:
                if (validar_session_admin()):
                    precio = float(precio)
                    respuesta, code = peliculas_controller.insertar_pelicula(nombre, sinopsis, categoria, precio)
                else: 
                    respuesta = {"status": "Forbidden"}
                    code = 403
            else:
                respuesta = {"status": "Bad request"}
                code = 401
        else:
            respuesta = {"status": "Bad request"}
            code = 401
    else:
        respuesta = {"status": "Bad request"}
        code = 401
    
    response = make_response(json.dumps(respuesta, cls=Encoder))  
    return response

@app.route("/api/peliculas/<int:id>", methods=["DELETE"])
def eliminar_pelicula(id):
    if (validar_session_admin()):
        respuesta, code = peliculas_controller.eliminar_pelicula(id)
    else:
        respuesta = {"status": "Forbidden"}
        code = 403
    response = make_response(json.dumps(respuesta, cls=Encoder), code)
    return response

@app.route("/api/peliculas/<int:id>", methods=["PUT"])
def actualizar_pelicula(id):
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        pelicula_json = request.json
        if "nombre" in pelicula_json and "sinopsis" in pelicula_json and "categoria" in pelicula_json and "precio" in pelicula_json:
            nombre = sanitize_input(pelicula_json["nombre"])
            sinopsis = sanitize_input(pelicula_json["sinopsis"])
            categoria = sanitize_input(pelicula_json["categoria"])
            precio = pelicula_json["precio"]

            # Validación de los parámetros
            if isinstance(nombre, str) and isinstance(sinopsis, str) and isinstance(categoria, str) and isinstance(precio, (int, float)) and len(nombre) < 128 and len(sinopsis) < 512 and len(categoria) < 512:
                if (validar_session_admin()):
                    # Llamar al controlador para actualizar la película
                    respuesta, code = peliculas_controller.actualizar_pelicula(id, nombre, sinopsis, categoria, precio)
                else:
                    respuesta = {"status": "Forbidden"}
                    code = 403
            else:
                app.logger.info("1")
                respuesta = {"status": "Bad request"}
                code = 401
        else:
            app.logger.info("2")
            respuesta = {"status": "Bad request"}
            code = 401
    else:
        app.logger.info("3")
        respuesta = {"status": "Bad request"}
        code = 401

    response = make_response(json.dumps(respuesta, cls=Encoder), code)
    return response

