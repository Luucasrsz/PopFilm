from __future__ import print_function
from bd import obtener_conexion
import sys

def insertar_juego(nombre, descripcion, precio,foto):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO juegos(nombre, descripcion, precio,foto) VALUES (%s, %s, %s,%s)",
                       (nombre, descripcion, precio,foto))
            if cursor.rowcount == 1:
                ret={"status": "OK" }
            else:
                ret = {"status": "Failure" }
        code=200
        conexion.commit()
        conexion.close()
    except:
        print("Excepcion al insertar un juego", file=sys.stdout)
        ret = {"status": "Failure" }
        code=500
    return ret,code

def convertir_juego_a_json(juego):
    d = {}
    d['id'] = juego[0]
    d['nombre'] = juego[1]
    d['descripcion'] = juego[2]
    d['precio'] = juego[3]
    d['foto'] = juego[4]
    return d

def obtener_juegos():
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre, descripcion, precio,foto FROM juegos")
            juegos = cursor.fetchall()
            juegosjson=[]
            if juegos:
                for juego in juegos:
                    juegosjson.append(convertir_juego_a_json(juego))
        conexion.close()
        code=200
    except:
        print("Excepcion al obtener los juegos", file=sys.stdout)
        juegosjson=[]
        code=500
    return juegosjson,code

def obtener_juego_por_id(id):
    juegojson = {}
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            #cursor.execute("SELECT id, nombre, descripcion, precio,foto FROM juegos WHERE id = %s", (id,))
            cursor.execute("SELECT id, nombre, descripcion, precio,foto FROM juegos WHERE id =" + id)
            juego = cursor.fetchone()
            if juego is not None:
                juegojson = convertir_juego_a_json(juego)
        conexion.close()
        code=200
    except:
        print("Excepcion al recuperar un juego", file=sys.stdout)
        code=500
    return juegojson,code


def eliminar_juego(id):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM juegos WHERE id = %s", (id,))
            if cursor.rowcount == 1:
                ret={"status": "OK" }
            else:
                ret={"status": "Failure" }
        conexion.commit()
        conexion.close()
        code=200
    except:
        print("Excepcion al eliminar un juego", file=sys.stdout)
        ret = {"status": "Failure" }
        code=500
    return ret,code

def actualizar_juego(id, nombre, descripcion, precio, foto):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE juegos SET nombre = %s, descripcion = %s, precio = %s, foto=%s WHERE id = %s",
                       (nombre, descripcion, precio, foto,id))
            if cursor.rowcount == 1:
                ret={"status": "OK" }
            else:
                ret={"status": "Failure" }
        conexion.commit()
        conexion.close()
        code=200
    except:
        print("Excepcion al eliminar un juego", file=sys.stdout)
        ret = {"status": "Failure" }
        code=500
    return ret,code
