<<<<<<< HEAD
import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv  

load_dotenv()

API_UID = os.getenv("API_UID")
API_TOKEN = os.getenv("API_TOKEN")
BASE_URL = os.getenv("BASE_URL")

 
app = Flask(__name__)




def get_script(movie_name):
    params = { 
        "uid": API_UID,
        "tokenid": API_TOKEN,
        "term": movie_name,
        "format": "json"
    }
    
    headers = {"User-Agent": "Mozilla/5.0"}  
    response = requests.get(BASE_URL, params=params, headers=headers)
    
    if response.status_code == 200:
        return response.json()  
    else:
        return {"error": f"Failed to fetch data: {response.status_code}", "details": response.text}

@app.route('/script', methods=['GET'])
def fetch_script():
    movie_name = request.args.get("movie")  
    
    if not movie_name:
        return jsonify({"error": "Missing 'movie' query parameter"}), 400
    
    data = get_script(movie_name)
    return jsonify(data)

@app.route('/')
def index():
    return "Welcome to the Movie Script API! scripts."

if __name__ == '__main__':
    app.run(debug=True)
=======


from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello Flask!'

if __name__ == '__main__':
    app.run()
>>>>>>> afd4f49a9ec0868b6a603631194407d503e2a3c8
