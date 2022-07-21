from flask import Flask, request
import jwt
import sys

app = Flask(__name__)

@app.before_first_request
def load_key():
    global secret_key
    with open("secret_key.key", "r") as f:
        secret_key = f.read()
        if len(secret_key) < 3:
            print("key is too short or does not exist, run gen_secret.py")
            shutdown = request.environ.get('werkzeug.server.shutdown')
            shutdown()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>" + secret_key


