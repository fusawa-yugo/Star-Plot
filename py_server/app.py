from flask import Flask, request, jsonify
from http import HTTPStatus
import os
import json
import base64

from plot_functions import skeletalize_points, match_skeleton_from_points

app = Flask(__name__)

UPLOAD_FOLDER = './input/images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET"])
def index():
    """
    サーバーが起動していることを確認するためのエンドポイント
    :return: サーバーが起動していることを示すメッセージ
    """
    return jsonify({"message": "Server is running"}), HTTPStatus.OK


@app.route("/skeletal-points", methods=["POST"])
def skeletal_points():
    """
    Base64で受け取った画像をデコードし、処理を行います。
    :return: JSON形式で処理結果を返します。
    """
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({'message': 'No image data provided'}), HTTPStatus.BAD_REQUEST

    try:
        img_binary = base64.b64decode(data['image'])
    except Exception as e:
        return jsonify({'message': 'Invalid Base64 image data'}), HTTPStatus.BAD_REQUEST

    keypoints = skeletalize_points(img_binary)
    if keypoints is None:
        return jsonify({'message': 'Failed to process the image'}), HTTPStatus.INTERNAL_SERVER_ERROR

    response = {
        'name': keypoints['name'],
        'skelton': keypoints['skelton'],
        'keypoints': keypoints['keypoints'],
        'valid': keypoints['valid']
    }
    return jsonify(response), HTTPStatus.OK


@app.route("/points-to-plot", methods=["POST"])
def points_to_plot():
    """
    Base64で受け取った画像とJSONデータを処理します。
    :return: JSON形式で処理結果を返します。
    """
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No image or JSON data provided'}), HTTPStatus.BAD_REQUEST

    try:
        img_binary = base64.b64decode(data['image'])
    except Exception as e:
        return jsonify({'message': 'Invalid Base64 image data'}), HTTPStatus.BAD_REQUEST

    try:
        edges = data.get('edges')
        nodes = data.get('nodes')
    except Exception as e:
        return jsonify({'message': 'Invalid JSON'}), HTTPStatus.BAD_REQUEST

    if not edges or not nodes:
        return jsonify({'message': 'No points provided in the JSON data'}), HTTPStatus.BAD_REQUEST

    plot_datas = match_skeleton_from_points(edges, nodes, img_binary)
    if plot_datas is None:
        return jsonify({'message': 'Failed to process the points'}), HTTPStatus.INTERNAL_SERVER_ERROR

    encoded_plots = [base64.b64encode(plot).decode('utf-8') for plot in plot_datas]

    response = {
        'plots': encoded_plots
    }
    return jsonify(response), HTTPStatus.OK
