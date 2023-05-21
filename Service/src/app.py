from crypt import methods
from http.client import BAD_GATEWAY, OK
from urllib import response
from wsgiref.util import request_uri
import json as JSON
from github_caller import GH
from flask import Flask, jsonify, request, session
from cachetools import cached, TTLCache

cache = TTLCache(maxsize=100, ttl=360)
import logging

logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s')

app = Flask(__name__)
app.debug = True
app.secret_key = 'super secret key'
gh = GH(logging)

@app.route("/")
def index():
    runs = gh.getCurrentRun()
    return jsonify(runs)

@app.route("/payload", methods=["POST"])
def protectionRule():
    json = request.get_json()
    session['payload'] = json
    return 'started', 200

@app.route("/callback", methods=["GET"])
def getCallback():
    callback = session['payload']['deployment_callback_url']
    return f"{callback}", 200

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
    if int(data["CPU"]) > 50:
        print(f"CPU HIGH")
        callback = session['payload']['deployment_callback_url']
        gh.rejectViaApp(callback)
    return f'{data}', 200
