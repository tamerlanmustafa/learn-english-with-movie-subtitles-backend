import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from script_fetcher import fetch_script_data

load_dotenv()

API_UID = os.getenv("API_UID")
API_TOKEN = os.getenv("API_TOKEN")
BASE_URL = os.getenv("BASE_URL")

app = Flask(__name__)


@app.route('/script', methods=['GET'])
def fetch_script():
    movie_name = request.args.get("movie")
    
    if not movie_name:
        return jsonify({"error": "Missing 'movie' query parameter"}), 400

    if not API_UID or not API_TOKEN or not BASE_URL:
        return jsonify({"error": "API credentials or base URL not set in environment variables."}), 500

    script_text = fetch_script_data(movie_name, API_UID, API_TOKEN, BASE_URL)
    return jsonify({"script": script_text})


@app.route('/')
def index():
    return "🎬 Welcome to the Movie Script API! Add ?movie=The+Matrix to /script."


if __name__ == '__main__':
    app.run(debug=True)
