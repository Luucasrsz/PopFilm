import os
from logging.config import dictConfig
from flask import Flask,request
from flask_wtf.csrf import CSRFProtect
from funciones_auxiliares import prepare_response_extra_headers


app = Flask(__name__)
app.config.from_pyfile('settings.py')
csrf = CSRFProtect(app)

#Configuración de las sesiones con cookies
app.config.update(PERMANENT_SESSION_LIFETIME=600)
app.config.update( SESSION_COOKIE_SECURE=True,   SESSION_COOKIE_HTTPONLY=True,   SESSION_COOKIE_SAMESITE='Lax',)


@app.errorhandler(500)
def server_error(error):
    app.logger.exception('An exception occurred during a request.')
    return 'Internal Server Error', 500

@app.before_request
def csrf_protect():
    if not request.path.startswith("/api/login") and not request.path.startswith("/api/registro"):
        csrf.protect()

#Configuración de la cabecera
extra_headers=prepare_response_extra_headers(True)

@app.after_request
def afterRequest(response):
    response.headers['Server'] = 'API'
    app.logger.info(
        "path: %s | method: %s | status: %s | size: %s >>> %s",
        request.path,
        request.method,
        response.status,
        response.content_length,
        request.remote_addr,
    )
    response.headers.extend(extra_headers)
    return response

from routes import ruta_inicio
from routes import ruta_peliculas

if __name__ == '__main__':
    port = int(os.environ.get('PORT'))
    host = os.environ.get('HOST')
    app.run(host=host, port=port)
