from flask import request, jsonify
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
         if "nombre" in pelicula_json and "sinopsis" in pelicula_json and "portada" in pelicula_json and "categoria" in pelicula_json:
            nombre = sanitize_input(pelicula_json["nombre"])
            sinopsis = sanitize_input(pelicula_json["sinopsis"])
            precio = pelicula_json["precio"]
            portada = sanitize_input(pelicula_json["portada"])
            categoria = sanitize_input(pelicula_json["categoria"])
         
            if isinstance(nombre, str) and isinstance(sinopsis, str) and isinstance(portada, str) and isinstance(categoria, str) and len(nombre)<128 and len(sinopsis)<512 and len(portada)<128 and len(categoria)<512:
                if (validar_session_admin()):
                    precio = float(precio)
                    respuesta,code=peliculas_controller.insertar_pelicula(nombre, sinopsis, categoria, precio, portada)
                else: 
                    respuesta={"status":"Forbidden"}
                    code=403
            else:
                respuesta={"status":"Bad request"}
                code=401
        else:
            respuesta={"status":"Bad request"}
            code=401
    else:
        respuesta={"status":"Bad request"}
        code=401
    response= make_response(json.dumps(respuesta, cls=Encoder))  
    return response
            
            

@app.route("/api/peliculas/<id>", methods=["DELETE"])
def eliminar_pelicula(id):
    # Sanitizar el ID antes de utilizarlo
    id = sanitize_input(id)
    ret, code = peliculas_controller.eliminar_pelicula(id)
    return ret, code  # No se necesita jsonify aquí.

@app.route("/api/peliculas", methods=["PUT"])
def actualizar_pelicula():
    content_type = request.headers.get('Content-Type')
    
    if 'multipart/form-data' in content_type:
        try:
            # Obtener los datos del formulario
            id = request.form.get('id')
            nombre = request.form.get('nombre')
            sinopsis = request.form.get('sinopsis')
            categoria = request.form.get('categoria')
            precio = request.form.get('precio')  # Asegúrate de obtener el precio como cadena
            
            if not id or not nombre or not sinopsis or not categoria or not precio:
                raise ValueError("Faltan campos requeridos")

            # Convertir precio a float
            try:
                precio = float(precio)
            except ValueError:
                raise ValueError("El precio debe ser un número válido")
            
            portada = request.files.get('portada')  # 'portada' es el campo donde se sube la imagen
            
            portada_filename = None
            if portada:
                # Definir la carpeta de destino
                upload_folder = 'uploads/'
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                
                # Guardar el archivo
                portada_filename = os.path.join(upload_folder, portada.filename)
                portada.save(portada_filename)
            
            # Llamada al controlador para actualizar la película
            ret, code = peliculas_controller.actualizar_pelicula(id, nombre, sinopsis, categoria, precio, portada_filename)
        
        except Exception as e:
            ret = {"status": "error", "message": str(e)}
            code = 500  # Internal Server Error
    else:
        ret = {"status": "Bad request", "message": "Content-Type must be multipart/form-data"}
        code = 400  # Bad Request
    
    return ret, code  # Retornar respuesta, no es necesario jsonify
