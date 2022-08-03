import sys
import random
from functools import wraps
from flask_cors import CORS
from datetime import datetime

import requests
from requests.auth import HTTPBasicAuth

from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, jsonify

import json
import jwt

import pymongo

app = Flask(__name__)
CORS(app)

@app.before_first_request
def setup_apis():
    global secret_key
    global db
    global watsonapi
    global rec_db

    with open("secret_key.key", "r") as f:
        secret_key = f.read()
        if len(secret_key) < 3:
            print("key is too short or does not exist, run gen_secret.py")
            shutdown = request.environ.get('werkzeug.server.shutdown')
            shutdown()
    with open("config.json", "r") as f:
        config = json.load(f)
    with open("Recommender System/csvjson.json") as f:
        rec_db = json.load(f)
    client = pymongo.MongoClient(config['database_link'])
    db = client.app
    watsonapi = config['watson']


def require_jwt(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = str(request.headers['Authorization'])
        try:
            token = jwt.decode(token, secret_key, algorithms=['HS256'])
        except jwt.exceptions.PyJWTError as e:
            return jsonify({"error":str(e)}), 401
        kwargs['username'] = token['username']
        return f(*args, **kwargs)
    return wrapper

@app.route('/get-recs', methods=['POST'])
@require_jwt
def get_recs(username):
    return jsonify([random.choice(rec_db) for x in range(4)])

def get_sentiment(feedback):
    data = {
      "text": feedback,
      "features": {
        "keywords": {
          "emotion": True
        }
      }
    }

    print(json.dumps(data))
    req = requests.post(watsonapi['url'], data=json.dumps(data),
            headers = {"Content-Type": "application/json"},
            auth=HTTPBasicAuth('apikey', watsonapi['apikey']))
    return req.json(), req.status_code

@app.route('/store-feedback-sentiment', methods=['POST'])
@require_jwt
def store_feedback_sentiment(username):
    feedback = request.json['feedback']
    time_spent = request.json['time-spent']
    sentiment, status = get_sentiment(feedback)
    sentiment = sentiment['keywords'][0]
    print(sentiment)
    sentiment['ibm'] = 'this is ibm\'s response btw'
    # TODO: actually store it somewhere

    happiness = sentiment['emotion']['joy']

    db.app.update_one({'username': username}, {'$push' : {'graph_data': 
        {'happiness': happiness, 'time_spent': time_spent, 'time': datetime.now()}}})

    return sentiment

@app.route('/graph-data', methods=['GET'])
@require_jwt
def graph_data(username):
    return jsonify(db.app.find_one({'username': username})['graph_data'])

@app.route("/signin", methods=['POST'])
def signin():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        user = db.app.find_one({'username': username})
        if not user:
            return jsonify({"error": "No such user"}), 409
        if not check_password_hash(user['password'], password):
            return jsonify({"error": "Wrong password"}), 409

        token = jwt.encode({'username':username}, secret_key, algorithm="HS256")

        return jsonify({"jwt": token})

@app.route("/signup", methods=['POST'])
def signup():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        user = db.app.find_one({'username': username})
        if not user:
            user = {'username': username, 
                'password': generate_password_hash(password),
                'graph_data': []}
            result = db.app.insert_one(user)
            return jsonify({'success': result is not None})
        if user:
            return jsonify({'error': 'user already exists'}), 409

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>" + secret_key

#flask run -h 0.0.0.0 -p 3000

