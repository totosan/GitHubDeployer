from github_caller import GH
from flask import Flask, jsonify, redirect, render_template, Response

app = Flask(__name__)

gh = GH()

@app.route("/")
def index():
    return 'Good', 200

@app.route("/cancel")
def cancel():
    return 'Cancelled', 200

@app.route("/ping")
def ping():
    return 'Pong', 200