from __future__ import print_function
from bd import obtener_conexion
import sys

def insertar_pelicula(nombre, sinopsis, categoria, precio, portada):
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO peliculas(nombre, sinopsis, categoria, precio, portada) VALUES (%s, %s, %s, %s, %s)",
                           (nombre, sinopsis, categoria, precio, portada))
            if cursor.rowcount == 1:
                ret = {"status": "OK"}
            else:
                ret = {"status": "Failure"}
        conexion.commit()
        code = 200
    except Exception as e:
        print(f"Excepcion al insertar una pelicula: {e}", file=sys.stdout)
        ret = {"status": "Failure"}
        code = 500
    finally:
        if conexion:
            conexion.close()
    return ret, code



def convertir_pelicula_a_json(pelicula):
    d = {}
    d['id'] = pelicula[0]
    d['nombre'] = pelicula[1]
    d['sinopsis'] = pelicula[2]
    d['categoria'] = pelicula[3]
    d['precio'] = pelicula[4]
    d['portada'] = pelicula[5]
    return d

def obtener_peliculas():
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre, sinopsis, categoria,precio, portada FROM peliculas")
            peliculas = cursor.fetchall()
            peliculasjson=[]
            if peliculas:
                for pelicula in peliculas:
                    peliculasjson.append(convertir_pelicula_a_json(pelicula))
        conexion.close()
        code=200
    except:
        print("Excepcion al obtener los juegos", file=sys.stdout)
        peliculasjson=[]
        code=500
    return peliculasjson,code

def obtener_pelicula_por_id(id):
    peliculasjson = {}
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre, sinopsis, categoria,precio, portada FROM peliculas WHERE id = %s", (id,))
            pelicula = cursor.fetchone()
            if pelicula is not None:
                peliculasjson = convertir_pelicula_a_json(pelicula)
        conexion.close()
        code=200
    except:
        print("Excepcion al recuperar una pelicula", file=sys.stdout)
        code=500
    return peliculasjson,code


def eliminar_pelicula(id):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM peliculas WHERE id = %s", (id,))
            if cursor.rowcount == 1:
                ret={"status": "OK" }
            else:
                ret={"status": "Failure" }
        conexion.commit()
        conexion.close()
        code=200
    except:
        print("Excepcion al eliminar una pelicula", file=sys.stdout)
        ret = {"status": "Failure" }
        code=500
    return ret,code

def actualizar_pelicula(id, nombre, sinopsis, categoria, precio, portada):
def actualizar_pelicula(id, nombre, sinopsis, categoria, precio, portada):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE peliculas SET nombre = %s, sinopsis = %s, categoria = %s, precio=%s, portada=%s WHERE id = %s",
                       (nombre, sinopsis, categoria, precio, portada, id))
            if cursor.rowcount == 1:
                ret = {"status": "OK"}
            else:
                ret = {"status": "Failure"}
        conexion.commit()
        conexion.close()
        code = 200
    except Exception as e:
        print(f"Excepcion al actualizar una pelicula: {e}", file=sys.stdout)
        ret = {"status": "Failure"}
        code = 500
    return ret, code

