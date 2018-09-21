from func.index import get_exif_data_for_folder
import os
from flask import Flask, jsonify, make_response, send_from_directory

# Configuration
image_dir = os.getcwd() + "/images" # TODO: probably a better way
current_dir = os.getcwd()

# Flask
app = Flask(__name__)

@app.route("/")
def get_exif_data():
    data = get_exif_data_for_folder(image_dir, current_dir)

    resp = make_response(jsonify(data))

    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp

@app.route('/images/<path:path>')
def send_js(path):
    return send_from_directory('images', path)