import os
from flask import Flask

app = Flask(__name__)

app.config.from_pyfile('settings.py')

from routes import ruta_inicio
from routes import ruta_peliculas
from routes import ruta_upload

if __name__ == '__main__':
    port = int(os.environ.get('PORT'))
    host = os.environ.get('HOST')
    app.run(host=host, port=port)
