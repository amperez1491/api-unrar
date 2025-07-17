from flask import Flask, request, send_file, jsonify
import rarfile
import tempfile
import os
import zipfile
import shutil

app = Flask(__name__)

@app.route('/unrar', methods=['POST'])
def unrar_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No se envió ningún archivo'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'Nombre de archivo vacío'}), 400

    if not file.filename.lower().endswith('.rar'):
        return jsonify({'error': 'El archivo no es un .rar válido'}), 400

    with tempfile.TemporaryDirectory() as temp_dir:
        rar_path = os.path.join(temp_dir, file.filename)
        file.save(rar_path)

        try:
            with rarfile.RarFile(rar_path) as rf:
                rf.extractall(temp_dir)
        except Exception as e:
            return jsonify({'error': f'Error al descomprimir: {str(e)}'}), 500

        zip_path = os.path.join(temp_dir, 'contenido_descomprimido')
        shutil.make_archive(zip_path, 'zip', temp_dir)

        return send_file(
            zip_path + '.zip',
            as_attachment=True,
            download_name='contenido_descomprimido.zip'
        )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)