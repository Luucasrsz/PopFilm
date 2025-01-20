import os
from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route("/")
def serve_index():
    return send_from_directory('/var/www/html', 'index.html')

@app.route("/api/")
def root():
    return "API Root"

app.config.from_pyfile('settings.py')

from routes import ruta_inicio
from routes import ruta_peliculas

if __name__ == '__main__':
    port = int(os.environ.get('PORT'))
    host = os.environ.get('HOST')
    app.run(host=host, port=port)
