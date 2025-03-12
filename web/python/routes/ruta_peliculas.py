from flask import request, jsonify
import os
import decimal
import json
from __main__ import app
from controllers import peliculas_controller
from funciones_auxiliares import sanitize_input

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super().default(obj)

@app.route("/api/peliculas", methods=["GET"])
def peliculas():
    peliculas, code = peliculas_controller.obtener_peliculas()
    return json.dumps(peliculas, cls=Encoder), code  # Usar json.dumps con el encoder


@app.route("/api/pelicula/<id>", methods=["GET"])
def pelicula_por_id(id):
    # Sanitizar el ID antes de utilizarlo
    id = sanitize_input(id)
    pelicula, code = peliculas_controller.obtener_pelicula_por_id(id)
    return json.dumps(pelicula, cls=Encoder), code  # Usar json.dumps con el encoder

@app.route("/api/peliculas", methods=["POST"])
def guardar_pelicula():
    content_type = request.headers.get('Content-Type')
    
    # Verificamos si el contenido es 'multipart/form-data', que es lo necesario para enviar archivos
    if 'multipart/form-data' in content_type:
        try:
            # Obtenemos los datos del formulario
            nombre = request.form['nombre']
            sinopsis = request.form['sinopsis']
            categoria = request.form['categoria']
            precio = request.form['precio']
            
            # Procesamos el archivo (portada)
            portada = request.files['portada']  # 'portada' es el nombre del campo del formulario
            
            # Procesar y guardar la imagen
            portada_filename = None
            if portada:
                # Definir la carpeta donde guardar las imágenes
                upload_folder = 'uploads/'
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                
                # Guardar el archivo con su nombre original
                portada_filename = os.path.join(upload_folder, portada.filename)
                portada.save(portada_filename)

                print(f"Imagen guardada en: {portada_filename}")  # Depuración
            
            # Llamar al controlador para insertar la película en la base de datos
            ret, code = peliculas_controller.insertar_pelicula(nombre, sinopsis, categoria, precio, portada_filename)
        except Exception as e:
            ret = {"status": "error", "message": str(e)}
            code = 500
    else:
        ret = {"status": "Bad request", "message": "Content-Type must be multipart/form-data"}
        code = 400  # Bad request en lugar de 401 para los casos incorrectos
    
    return ret, code  # No se necesita jsonify aquí.

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
