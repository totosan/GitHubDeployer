from crypt import methods
from http.client import BAD_GATEWAY, OK
from urllib import response
from wsgiref.util import request_uri

from github_caller import GH
from flask import Flask, jsonify, request
import logging

logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s')

app = Flask(__name__)
app.debug = True
gh = GH(logging)


@app.route("/")
def index():
    runs = gh.getCurrentRun()
    return jsonify(runs)

@app.route("/payload", methods=["POST"])
def protectionRule():#b324b207f46ba3cb0d15164f70d5eab326107b4b
    json = request.get_json()
    
    return 'started', 200

@app.route("/start", methods=["POST"])
def startWF():
    startJson = request.get_json()
    isRing=startJson['isTerminator']
    ret = gh.startWF(isRing)
    if ret:
        return 'started', 200
    else:
        return 'not started', 501


@app.route("/cancel", methods=['POST'])
def cancel():
    gh.getCurrentRun()
    gh.cancel()
    return 'Cancelled', 200


@app.route("/approve", methods=['POST'])
def approve():
    gh.getCurrentRun()
    gh.approve()
    return 'approved', 200


@app.route("/reject", methods=['POST'])
def reject():
    gh.getCurrentRun()
    gh.reject()
    return 'rejected', 200


@app.route("/ping")
def ping():
    return 'Pong', 200


@app.route("/simulateError", methods=['POST'])
def simulateError():
    data = request.get_json()
    print(data)
    print(f"CPU HIGH")
    return f'{data}', 200
