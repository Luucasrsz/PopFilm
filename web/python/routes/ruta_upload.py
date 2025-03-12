from flask import Flask, request, jsonify
from bd import obtener_conexion
import os
import uuid
from funciones_auxiliares import sanitize_input

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Verificar que el archivo tiene una extensión permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Ruta para subir la portada de la película
@app.route('/api/upload_image', methods=['POST'])
def upload_portada():
    if 'file' not in request.files:
        return jsonify({"status": "ERROR", "message": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"status": "ERROR", "message": "No selected file"}), 400

    if 'pelicula_id' not in request.form:
        return jsonify({"status": "ERROR", "message": "No pelicula_id provided"}), 400

    pelicula_id = request.form['pelicula_id']

     # Sanitizar el pelicula_id para prevenir entradas maliciosas
    pelicula_id = sanitize_input(pelicula_id)
    
    if file and allowed_file(file.filename):
        # Crear un nombre único para el archivo
        filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Guardar el archivo en el servidor
        file.save(file_path)

        # Insertar en la tabla 'portadas' y vincularla con la película
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO portadas (pelicula_id, ruta_portada)
            VALUES (%s, %s)
        ''', (pelicula_id, filename))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"status": "OK", "message": "Portada subida exitosamente", "file_path": file_path}), 200

    else:
        return jsonify({"status": "ERROR", "message": "File type not allowed"}), 400

if __name__ == "__main__":
    app.run(debug=True)