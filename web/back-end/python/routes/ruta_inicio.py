from flask import request, session
from bd import obtener_conexion
from __main__ import app
import json
from bcrypt import hashpw, gensalt, checkpw  # Para manejar contraseñas de forma segura

@app.route("/api/login", methods=['POST'])
def login():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        usuario_json = request.json
        email = usuario_json.get('email')
        contrasena = usuario_json.get('contrasena')

        try:
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                # Consulta segura con parámetros
                cursor.execute("SELECT contrasena, perfil FROM usuarios WHERE email = %s", (email,))
                usuario = cursor.fetchone()

                if usuario is None or not checkpw(password.encode('utf-8'), usuario[0].encode('utf-8')):
                    ret = {"status": "ERROR", "mensaje": "Usuario o contraseña incorrectos"}
                else:
                    # Actualiza la columna logeado
                    cursor.execute("UPDATE usuarios SET logeado = TRUE WHERE email = %s", (email,))
                    conexion.commit()

                    ret = {"status": "OK"}
                    session["usuario"] = email
                    session["perfil"] = usuario[1]
            code = 200
        except Exception as e:
            print(f"Excepción al validar al usuario: {str(e)}")
            ret = {"status": "ERROR", "mensaje": "Error interno del servidor"}
            code = 500
        finally:
            conexion.close()
    else:
        ret = {"status": "Bad request", "mensaje": "Formato de contenido no válido"}
        code = 400
    return json.dumps(ret), code


@app.route("/api/registro", methods=['POST'])
def registro():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        usuario_json = request.json
        email = usuario_json.get('email')
        contrasena = usuario_json.get('contrasena')
        nombre = usuario_json.get('nombre')
        perfil = usuario_json.get('profile')

        try:
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                # Verifica si el usuario ya existe
                cursor.execute("SELECT email FROM usuarios WHERE email = %s", (email,))
                usuario = cursor.fetchone()

                if usuario is None:
                    # Cifrar la contraseña
                    hashed_password = hashpw(contrasena.encode('utf-8'), gensalt()).decode('utf-8')

                    cursor.execute(
                        "INSERT INTO usuarios (email, contrasena, nombre, perfil, logeado) VALUES (%s, %s, %s, %s, FALSE)",
                        (email, hashed_password, nombre, perfil)
                    )
                    if cursor.rowcount == 1:
                        conexion.commit()
                        ret = {"status": "OK", "mensaje": "Usuario registrado correctamente"}
                        code = 201
                    else:
                        ret = {"status": "ERROR", "mensaje": "No se pudo registrar el usuario"}
                        code = 500
                else:
                    ret = {"status": "ERROR", "mensaje": "El usuario ya existe"}
                    code = 400
        except Exception as e:
            print(f"Excepción al registrar al usuario: {str(e)}")
            ret = {"status": "ERROR", "mensaje": "Error interno del servidor"}
            code = 500
        finally:
            conexion.close()
    else:
        ret = {"status": "Bad request", "mensaje": "Formato de contenido no válido"}
        code = 400
    return json.dumps(ret), code


@app.route("/api/logout", methods=['GET'])
def logout():
    try:
        if "usuario" in session:
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                # Deslogea al usuario en la base de datos
                cursor.execute("UPDATE usuarios SET logeado = FALSE WHERE email = %s", (session["usuario"],))
                conexion.commit()
            conexion.close()

        session.clear()
        ret = {"status": "OK", "mensaje": "Sesión cerrada correctamente"}
        code = 200
    except Exception as e:
        print(f"Excepción al cerrar sesión: {str(e)}")
        ret = {"status": "ERROR", "mensaje": "Error al cerrar sesión"}
        code = 500

    return json.dumps(ret), code
