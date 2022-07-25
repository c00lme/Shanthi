import sys
from functools import wraps

import requests
from requests.auth import HTTPBasicAuth

from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, jsonify

import json
import jwt

import pymongo

app = Flask(__name__)

@app.before_first_request
def setup_apis():
    global secret_key
    global db
    global watsonapi

    with open("secret_key.key", "r") as f:
        secret_key = f.read()
        if len(secret_key) < 3:
            print("key is too short or does not exist, run gen_secret.py")
            shutdown = request.environ.get('werkzeug.server.shutdown')
            shutdown()
    with open("config.json", "r") as f:
        config = json.load(f)
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
    return jsonify({'recs': ['https://www.youtube.com/watch?v=dQw4w9WgXcQ' for x in range(4)]})

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
    user = db.app.find_one({'username': username})
    if not user:
        return jsonify({"error": "No such user"})
    feedback = request.form['feedback']
    sentiment, status = get_sentiment(feedback)
    sentiment = sentiment['keywords'][0]
    print(sentiment)
    sentiment['ibm'] = 'this is ibm\'s response btw'
    # TODO: actually store it somewhere

    happiness = sentiment['emotion']['joy']

    # TODO: improve this
    # we have in sentiment['emotion']: "anger":0.789045,"disgust":0.045893,"fear":0.032463,"joy":0.015018,"sadness":0.047767
    # and we have sentiment['relavence']
    motivation = ( 0.5 *(1 - sentiment['emotion']['fear'])) + (0.5 * ( 1 - sentiment['emotion']['sadness']))
    print(f"motivation: {motivation}, happiness: {happiness}")

    return sentiment

@app.route("/signin", methods=['POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.app.find_one({'username': username})
        if not user:
            return jsonify({"error": "No such user"})
        if not check_password_hash(user['password'], password):
            return jsonify({"error": "Wrong password"})

        token = jwt.encode({'username':username}, secret_key, algorithm="HS256")

        return jsonify({"jwt": token})

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>" + secret_key


