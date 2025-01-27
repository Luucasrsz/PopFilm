from flask import request

@app.route('/api/upload', methods=['POST'])
def upload():
    try:
        # Verificar el Content-Type
        content_type = request.content_type
        if not content_type.startswith('multipart/form-data'):
            return json.dumps({"status": "ERROR", "message": "Content-Type debe ser 'multipart/form-data'"}), 400
        
        if 'portada' not in request.files:
            return json.dumps({"status": "ERROR", "message": "No se adjuntó un archivo"}), 400
        
        f = request.files['portada']  # Obtener el archivo
        user_input = request.form.get("nombre")  # Obtener el nombre de la película
        
        # Sanitizar el nombre de la película
        safe_name = user_input.replace(" ", "_").replace("/", "_").replace("\\", "_")
        
        basepath = os.path.dirname(__file__)
        upload_folder = os.path.join(basepath, 'uploads')  # Carpeta de archivos subidos
        
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        # Usar el nombre de la película para el archivo
        file_path = os.path.join(upload_folder, f"{safe_name}_{f.filename}")

        f.save(file_path)

        return json.dumps({"status": "OK", "file_path": file_path}), 200

    except Exception as e:
        return json.dumps({"status": "ERROR", "message": str(e)}), 500
