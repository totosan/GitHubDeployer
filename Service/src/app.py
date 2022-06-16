from http.client import OK
from urllib import request, response
from github_caller import GH
from flask import Flask, jsonify, redirect, render_template, Response
app = Flask(__name__)

@app.route("/")
def index():
    return 'Good', 200