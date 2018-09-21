from func.index import get_exif_data_for_folder
import os
from flask import Flask, jsonify

# Configuration
image_dir = os.getcwd() + "/images" # TODO: probably a better way

# Flask
app = Flask(__name__)

@app.route("/")
def get_exif_data():
    data = get_exif_data_for_folder(image_dir)

    return jsonify(data)