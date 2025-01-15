from flask import request, session
import json
import decimal
from __main__ import app
from controllers import peliculas_controller

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal): return float(obj)

@app.route("/peliculas",methods=["GET"])
def pelicuas():
    peliculas,code= peliculas_controller.obtener_peliculas()
    return json.dumps(peliculas, cls = Encoder),code

@app.route("/pelicula/<id>",methods=["GET"])
def pelicula_por_id(id):
    pelicula,code = peliculas_controller.obtener_pelicula_por_id(id)
    return json.dumps(pelicula, cls = Encoder),code

@app.route("/peliculas",methods=["POST"])
def guardar_pelicula():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        pelicula_json = request.json
        ret,code=peliculas_controller.insertar_pelicula(pelicula_json["nombre"], pelicula_json["sinopsis"], (pelicula_json["categoria"]), pelicula_json["portada"])
    else:
        ret={"status":"Bad request"}
        code=401
    return json.dumps(ret), code

@app.route("/peliculas/<id>", methods=["DELETE"])
def eliminar_pelicula(id):
    ret,code=peliculas_controller.eliminar_pelicula(id)
    return json.dumps(ret), code

@app.route("/peliculas", methods=["PUT"])
def actualizar_pelicula():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        pelicula_json = request.json
        ret,code=peliculas_controller.actualizar_pelicula(pelicula_json["id"],pelicula_json["nombre"], pelicula_json["sinopsis"], (pelicula_json["categoria"]),pelicula_json["portada"])
    else:
        ret={"status":"Bad request"}
        code=401
    return json.dumps(ret), code