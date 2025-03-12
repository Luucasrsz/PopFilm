from flask import Flask, request, jsonify, make_response
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from flask_cors import CORS
import pymysql
from bcrypt import hashpw, gensalt, checkpw
from bd import obtener_conexion
import os
import json
from funciones_auxiliares import sanitize_input

app = Flask(__name__)

# Configuración del JWT
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY')
app.config["JWT_TOKEN_LOCATION"] = ["cookies"] 
app.config["JWT_COOKIE_SECURE"] = False 
app.config["JWT_COOKIE_HTTPONLY"] = True  
app.config["JWT_COOKIE_SAMESITE"] = "Strict"

jwt = JWTManager(app)
CORS(app, supports_credentials=True)

@app.route("/api/login", methods=['POST'])
def login():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        usuario_json = request.json
        if "email" in usuario_json and "contrasena" in usuario_json:
            email = sanitize_input(usuario_json['email'])
            contrasena = sanitize_input(usuario_json['contrasena'])

        try:
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute("SELECT contrasena FROM usuarios WHERE email = %s", (email,))
                usuario = cursor.fetchone()

                if usuario is None or not checkpw(contrasena.encode('utf-8'), usuario[0].encode('utf-8')):
                    return jsonify({"status": "ERROR", "mensaje": "Usuario o contraseña incorrectos"}), 400

                # Generar el JWT
                token = create_access_token(identity=email)

                # Guardar en cookie segura
                resp = make_response(jsonify({"status": "OK"}))
                resp.set_cookie("access_token_cookie", token, httponly=True, samesite="Strict")
                return resp
        except Exception as e:
            print(f"Excepción al validar al usuario: {str(e)}")
            return jsonify({"status": "ERROR", "mensaje": "Error interno del servidor"}), 500
        finally:
            conexion.close()

    return jsonify({"status": "ERROR", "mensaje": "Formato de contenido no válido"}), 400



@app.route("/api/registro", methods=['POST'])
def registro():
    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json':
        return jsonify({"status": "ERROR", "mensaje": "Formato de contenido no válido"}), 400

    usuario_json = request.json
    email = usuario_json.get('email')
    contrasena = usuario_json.get('contrasena')
    nombre = usuario_json.get('nombre')

    email = sanitize_input(email)
    contrasena = sanitize_input(contrasena)
    nombre = sanitize_input(nombre)

    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT email FROM usuarios WHERE email = %s", (email,))
            usuario = cursor.fetchone()

            if usuario:
                return jsonify({"status": "ERROR", "mensaje": "El usuario ya existe"}), 400

            hashed_password = hashpw(contrasena.encode('utf-8'), gensalt()).decode('utf-8')
            cursor.execute(
                "INSERT INTO usuarios (email, contrasena, nombre) VALUES (%s, %s, %s)",
                (email, hashed_password, nombre)
            )
            if cursor.rowcount == 1:
                conexion.commit()
                return jsonify({"status": "OK", "mensaje": "Usuario registrado"}), 201

            return jsonify({"status": "ERROR", "mensaje": "No se pudo registrar el usuario"}), 500

    except Exception as e:
        print(f"Excepción al registrar al usuario: {str(e)}")
        return jsonify({"status": "ERROR", "mensaje": "Error interno del servidor"}), 500

    finally:
        conexion.close()


@app.route("/api/protegido", methods=["GET"])
@jwt_required()
def protegido():
    usuario = get_jwt_identity()
    return jsonify({"message": "Acceso permitido", "user": usuario})

# 🔹 LOGOUT - Elimina la cookie JWT
@app.route("/api/logout", methods=['POST'])
def logout():
    resp = make_response(jsonify({"status": "OK", "mensaje": "Sesión cerrada"}))
    resp.set_cookie("access_token_cookie", "", expires=0)  # Borra la cookie
    return resp

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)