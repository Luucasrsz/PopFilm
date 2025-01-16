import os
from flask import Flask
from variables import cargarvariables


app = Flask(__name__)

from routes import ruta_inicio
from routes import ruta_peliculas

app.config.from_pyfile('settings.py')
cargarvariables()

if __name__ == '__main__':
    port = int(os.environ.get('PORT'))
    host = os.environ.get('HOST')
    app.run(host=host, port=port)