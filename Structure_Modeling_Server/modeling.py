from flask import Flask, request, jsonify, send_from_directory, url_for
from flask_cors import CORS
from Mallado import Mallado
import os
import cv2
import numpy as np

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app, resources={r"/upload": {"origins": "http://localhost:3000"}})


@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        if 'image' not in request.files:
            return 'No se proporcionó ninguna imagen', 400
        
        image = request.files['image']

        if image.filename == '':
            return 'No se seleccionó ningún archivo', 400

        # Guarda la imagen en el directorio de subidas
        path_image = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(path_image)
        
        mallado = Mallado(path_image)
        mallado.cargar_imagen()
        gradient_x, gradient_y = mallado.imagen_BW()
        normals = mallado.direccion_normal(gradient_x=gradient_x, gradient_y=gradient_y)
        shading = mallado.producto_escalar(normals=normals)
        
        # Guarda la imagen procesada en el directorio de subidas
        path_processed_image = os.path.join(app.config['UPLOAD_FOLDER'], 'processed_' + image.filename)
        cv2.imwrite(path_processed_image, shading)
        
        processed_image_url = url_for('uploaded_file', filename='processed_' + image.filename, _external=True)
        
        return jsonify({'message': 'Imagen recibida y procesada', 'processed_image_url': processed_image_url})


    except Exception as e:
        return jsonify({'error': 'Error al procesar la imagen'}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)

