from github_caller import GH
from flask import Flask, jsonify

app = Flask(__name__)

gh = GH()

@app.route("/")
def index():
    runs=gh.getCurrentRun()
    return jsonify(runs)

@app.route("/cancel")
def cancel():
    return 'Cancelled', 200

@app.route("/ping")
def ping():
    return 'Pong', 200