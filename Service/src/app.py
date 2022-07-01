from crypt import methods
from github_caller import GH
from flask import Flask, jsonify

app = Flask(__name__)

gh = GH()

@app.route("/")
def index():
    runs=gh.getCurrentRun()
    return jsonify(runs)

@app.route("/cancel",methods=['POST'])
def cancel():
    gh.getCurrentRun()
    gh.cancel()
    return 'Cancelled', 200

@app.route("/approve",methods=['GET'])
def approve():
    gh.getCurrentRun()
    gh.approve()
    return 'approved', 200

@app.route("/reject",methods=['GET'])
def reject():
    gh.getCurrentRun()
    gh.reject()
    return 'rejected', 200

@app.route("/ping")
def ping():
    return 'Pong', 200

@app.route("/simulateError", methods=['POST'])
def simulateError(on):
    print(f"set simulation: {on}")
    return f'CPU {on}',200