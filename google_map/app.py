from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = "data.json"
GOOGLE_MAPS_API_KEY = "AIzaSyD2GY7IRyLB5UHhwLeiNe05pBHe1fd8SSI"

# Load existing data or initialize
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

def load_coordinates():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_coordinates(coords):
    with open(DATA_FILE, "w") as f:
        json.dump(coords, f)

@app.route("/")
def index_page():
    return render_template("index.html", GOOGLE_MAPS_API_KEY=GOOGLE_MAPS_API_KEY)

@app.route("/api/points", methods=["POST"])
def add_coordinate():
    data = request.get_json()
    lat = data.get("latitude")
    lng = data.get("longitude")

    if lat is None or lng is None:
        return jsonify({"error": "Missing latitude or longitude"}), 400

    coordinates = load_coordinates()
    coordinates.append({"lat": lat, "lng": lng})
    save_coordinates(coordinates)

    return jsonify({"success": True}), 201

@app.route("/api/points", methods=["GET"])
def get_coordinates():
    return jsonify(load_coordinates())

if __name__ == "__main__":
    app.run(debug=True,port=5004)




