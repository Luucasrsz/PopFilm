from __future__ import print_function
from bd import obtener_conexion
import sys

def insertar_pelicula(nombre, sinopsis, categoria, portada):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO peliculas(nombre, sinopsis, categoria, portada) VALUES (%s, %s, %s, %s)",
                       (nombre, sinopsis, categoria, portada))
            if cursor.rowcount == 1:
                ret={"status": "OK" }
            else:
                ret = {"status": "Failure" }
        code=200
        conexion.commit()
        conexion.close()
    except:
        print("Excepcion al insertar una pelicula", file=sys.stdout)
        ret = {"status": "Failure" }
        code=500
    return ret,code

def convertir_pelicula_a_json(pelicula):
    d = {}
    d['id'] = pelicula[0]
    d['nombre'] = pelicula[1]
    d['sinopsis'] = pelicula[2]
    d['categoria'] = pelicula[3]
    d['portada'] = pelicula[4]
    return d

def obtener_peliculas():
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre, sinopsis, categoria,portada FROM peliculas")
            peliculas = cursor.fetchall()
            peliculasjson=[]
            if peliculas:
                for pelicula in peliculas:
                    peliculasjson.append(convertir_pelicula_a_json(pelicula))
        conexion.close()
        code=200
    except:
        print("Excepcion al obtener los juegos", file=sys.stdout)
        juegosjson=[]
        code=500
    return juegosjson,code

def obtener_pelicula_por_id(id):
    juegojson = {}
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            #cursor.execute("SELECT id, nombre, descripcion, precio,foto FROM juegos WHERE id = %s", (id,))
            cursor.execute("SELECT id, nombre, sinopsis, categoria,portada FROM peliculas WHERE id =" + id)
            pelicula = cursor.fetchone()
            if pelicula is not None:
                peliculasJson = convertir_pelicula_a_json(pelicula)
        conexion.close()
        code=200
    except:
        print("Excepcion al recuperar una pelicula", file=sys.stdout)
        code=500
    return juegojson,code


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

def actualizar_pelicula(id, nombre, sinopsis, categoria, portada):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE juegos SET nombre = %s, sinopsis = %s, categoria = %s, portada=%s WHERE id = %s",
                       (nombre, sinopsis, categoria, portada,id))
            if cursor.rowcount == 1:
                ret={"status": "OK" }
            else:
                ret={"status": "Failure" }
        conexion.commit()
        conexion.close()
        code=200
    except:
        print("Excepcion al ectualizar una pelicula", file=sys.stdout)
        ret = {"status": "Failure" }
        code=500
    return ret,code
