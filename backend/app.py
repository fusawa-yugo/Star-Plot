from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from http import HTTPStatus
import os

app = Flask(__name__)

UPLOAD_FOLDER = './input/images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload-images', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part in the request'}), HTTPStatus.BAD_REQUEST
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), HTTPStatus.BAD_REQUEST
    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        return jsonify({'filename': filename}), HTTPStatus.OK
    except Exception as e:
        # 開発時のみエラーメッセージを返す（本番環境ではログのみ推奨）
        return jsonify({'message': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
