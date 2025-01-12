import os
from flask import Flask
from variables import cargarvariables
from routes import ruta_inicio
from routes import ruta_peliculas

app = Flask(__name__)

app.config.from_pyfile('settings.py')
cargarvariables()

if __name__ == '__main__':
    port = int(os.environ.get('PORT'))
    host = os.environ.get('HOST')
    app.run(host=host, port=port)