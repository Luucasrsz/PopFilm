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
    response= make_response(json.dumps(respuesta, cls=Encoder), code)  # Usar json.dumps con el encoder
    return response

@app.route("/api/pelicula/<id>", methods=["GET"])
def pelicula_por_id(id):
    # Sanitizar el ID antes de utilizarlo
    id = sanitize_input(id)
    if isinstance(id, str) and len(id)<64:
        if (validar_session_normal()):
            respuesta, code = peliculas_controller.obtener_pelicula_por_id(id)
        else:
            respuesta={"status":"Bad parameters"}
            code=403 
    
    response= make_response(json.dumps(respuesta, cls=Encoder), code)
    return response

@app.route("/api/peliculas", methods=["POST"])
def guardar_pelicula():
    content_type = request.headers.get('Content-Type')
    
    # Verificamos si el contenido es 'multipart/form-data', que es lo necesario para enviar archivos
    if (content_type == 'application/json'):
        pelicula_json = request.json
        # Asegúrate de que el if esté correctamente indentado
        if "nombre" in pelicula_json and "sinopsis" in pelicula_json and "portada" in pelicula_json and "categoria" in pelicula_json:
            nombre = sanitize_input(pelicula_json["nombre"])
            sinopsis = sanitize_input(pelicula_json["sinopsis"])
            precio = pelicula_json["precio"]
            portada = sanitize_input(pelicula_json["portada"])
            categoria = sanitize_input(pelicula_json["categoria"])
         
            if isinstance(nombre, str) and isinstance(sinopsis, str) and isinstance(portada, str) and isinstance(categoria, str) and len(nombre)<128 and len(sinopsis)<512 and len(portada)<128 and len(categoria)<512:
                if (validar_session_admin()):
                    precio = float(precio)
                    respuesta, code = peliculas_controller.insertar_pelicula(nombre, sinopsis, categoria, precio, portada)
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


@app.route("/api/peliculas", methods=["PUT"])
def actualizar_pelicula():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        pelicula_json = request.json
        # Verificamos si contiene los campos necesarios
        if "id" in pelicula_json and "nombre" in pelicula_json and "sinopsis" in pelicula_json and "categoria" in pelicula_json and "precio" in pelicula_json and "portada" in pelicula_json:
            id = pelicula_json["id"]
            nombre = sanitize_input(pelicula_json["nombre"])
            sinopsis = sanitize_input(pelicula_json["sinopsis"])
            categoria = sanitize_input(pelicula_json["categoria"])
            precio = pelicula_json["precio"]
            portada = sanitize_input(pelicula_json["portada"])

            # Validamos los datos
            if isinstance(id, int) and isinstance(nombre, str) and isinstance(sinopsis, str) and isinstance(categoria, str) and isinstance(precio, (int, float)) and isinstance(portada, str) and len(id) < 8 and len(nombre) < 128 and len(sinopsis) < 512 and len(categoria) < 512 and len(portada) < 128:
                if (validar_session_admin()):
                    # Llamada al controlador para actualizar la película
                    respuesta, code = peliculas_controller.actualizar_pelicula(id, nombre, sinopsis, categoria, precio, portada)
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

    response = make_response(json.dumps(respuesta, cls=Encoder), code)
    return response
