import json
from flask import Flask, request, session, make_response, Response
from flask_session import Session
from datetime import timedelta
from flask_cors import *
from web_sqlite import *
import os

app = Flask(__name__)
CORS(app, supports_credentials=True, resources=r"/*")
database = My_sqlite("studentList.db")
app.secret_key = os.urandom(24)


@app.route('/getStudnet', methods=["GET", "POST"])
def hello_world():
    datalist = []
    for i in getStudentInfo(database):
        datalist.append(dict(zip(["id", "name", "sex", "age", "address"], i)))
    return json.dumps({"data": datalist}), 200


@app.route("/login", methods=["POST"])
def login():
    user = request.get_json()["user"]
    password = request.get_json()["password"]
    if selPassword(database, user, password):
        res = make_response({"code": True})
        res.set_cookie("uname", user, 3600)
        return res, 200
    else:
        return json.dumps({"code": False}), 200


@app.route("/delStu", methods=["post"])
def delStu():
    user = request.get_json()["user"]
    if delStudent(database, user):
        return json.dumps({"code": True}), 200
    else:
        return json.dumps({"code": False}), 200


@app.route("/updataStu", methods=["post"])
def updataStu():
    data = request.get_json()["data"]
    upDataStudent(database, data["id"], data["name"], data["sex"], data["age"], data["address"])
    return json.dumps({"code": True}), 200


@app.route("/changePassword", methods=["post"])
def changePassword():
    user = request.get_json()["user"]
    pad = request.get_json()["password"]
    if chanGePassword(database, user, pad):
        return json.dumps({"code": True}), 200
    else:
        return json.dumps({"code", False}), 200


@app.route("/addStu", methods=["post"])
def addStu():
    data = request.get_json()["data"]
    print(data)
    intoStudentInfo(database, data["id"], data["name"], data["sex"], data["age"], data["address"])
    return json.dumps({"code": True}), 200


if __name__ == '__main__':
    app.run()
