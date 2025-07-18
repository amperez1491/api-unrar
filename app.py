from flask import Flask, request, send_file, jsonify
import rarfile
import tempfile
import os
import shutil

app = Flask(__name__)

# Configuración opcional: aumentar el límite de tamaño de archivo (ej. 1 GB)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024  # 1 GB

@app.route('/unrar', methods=['POST'])
def unrar_file():
    # Verificar que se haya enviado un archivo
    if 'file' not in request.files:
        return jsonify({'error': 'No se envió ningún archivo'}), 400

    file = request.files['file']

    # Verificar que el archivo tenga nombre
    if file.filename == '':
        return jsonify({'error': 'Nombre de archivo vacío'}), 400

    # Verificar que sea un archivo .rar
    if not file.filename.lower().endswith('.rar'):
        return jsonify({'error': 'El archivo no es un .rar válido'}), 400

    # Crear un directorio temporal para trabajar
    with tempfile.TemporaryDirectory() as temp_dir:
        # Guardar el archivo .rar en el directorio temporal
        rar_path = os.path.join(temp_dir, file.filename)
        file.save(rar_path)

        try:
            # Abrir y descomprimir el archivo .rar
            with rarfile.RarFile(rar_path) as rf:
                rf.extractall(temp_dir)
        except Exception as e:
            return jsonify({'error': f'Error al descomprimir el archivo: {str(e)}'}), 500

        # Crear un archivo .zip con el contenido descomprimido
        zip_path = os.path.join(temp_dir, 'contenido_descomprimido')
        shutil.make_archive(zip_path, 'zip', temp_dir)

        # Enviar el archivo .zip como descarga
        return send_file(
            zip_path + '.zip',
            as_attachment=True,
            download_name='contenido_descomprimido.zip',
            mimetype='application/zip'
        )

# Iniciar la aplicación
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
        )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
