import sys
from functools import wraps

from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, jsonify

import json
import jwt

import pymongo

app = Flask(__name__)

def open_database():
    with open("config.json", "r") as f:
        config = json.load(f)
        client = pymongo.MongoClient(config['database_link'])
        return client.app


@app.before_first_request
def load_key():
    global secret_key
    global db
    with open("secret_key.key", "r") as f:
        secret_key = f.read()
        if len(secret_key) < 3:
            print("key is too short or does not exist, run gen_secret.py")
            shutdown = request.environ.get('werkzeug.server.shutdown')
            shutdown()
    db = open_database()

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

@app.route('/get_recs', methods=['POST'])
@require_jwt
def get_recs(username):
    return jsonify({'recs': ['https://www.youtube.com/watch?v=dQw4w9WgXcQ' for x in range(4)]})

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


