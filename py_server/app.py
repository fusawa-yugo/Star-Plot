from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from http import HTTPStatus
import os

app = Flask(__name__)

UPLOAD_FOLDER = './input/images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/skeletal-points", methods=["POST"])
def skeletal_points():
    """
    受け取った画像のファイル名を取得し、指定されたフォルダに保存します。
    :return: JSON形式でファイル名を返します。
    """
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
