from flask import Flask, request, jsonify, g
from myjwt import *
from flask_cors import *
from web_sqlite import *

app = Flask(__name__)
CORS(app, supports_credentials=True, resources=r"/*")
database = My_sqlite("studentList.db")
app.config['JSON_AS_ASCII'] = False


@app.before_request
def my_before_request():
    token = request.headers.get("token")
    if token:
        if getToKen(token):
            g.Turntable = True
        else:
            g.Turntable = False
    else:
        g.Turntable = False


@app.route('/getStudnet', methods=["GET", "POST"])
def hello_world():
    datalist = []
    if g.Turntable:
        for i in getStudentInfo(database):
            datalist.append(dict(zip(["id", "name", "sex", "age", "address"], i)))
        return jsonify({"code": True, "data": datalist}), 200
    else:
        return jsonify({"code": False, "msg": "请先登录"})


@app.route("/login", methods=["POST"])
def login():
    user = request.get_json()["user"]
    password = request.get_json()["password"]
    print(user, password)
    if selPassword(database, user, password):
        token = setToKen(user)
        return jsonify({"code": True, "msg": "登录成功", "token": token}), 200
    else:
        return jsonify({"code": False, "msg": "账号密码错误"}), 200


@app.route("/delStu", methods=["post"])
def delStu():
    if g.Turntable:
        user = request.get_json()["user"]
        print(user)
        if delStudent(database, user):
            return jsonify({"code": True}), 200
        else:
            return jsonify({"code": False}), 200
    else:
        return jsonify({"code": False, "msg": "请先登录"})


@app.route("/updataStu", methods=["post"])
def updataStu():
    if g.Turntable:
        data = request.get_json()["data"]
        upDataStudent(database, data["id"], data["name"], data["sex"], data["age"], data["address"])
        return jsonify({"code": True}), 200
    else:
        return jsonify({"code": False, "msg": "请先登录"})


@app.route("/changePassword", methods=["post"])
def changePassword():
    if g.Turntable:
        user = request.get_json()["user"]
        pad = request.get_json()["password"]
        if chanGePassword(database, user, pad):
            return jsonify({"code": True}), 200
        else:
            return jsonify({"code", False}), 200
    else:
        return jsonify({"code": False, "msg": "请先登录"})


@app.route("/addStu", methods=["post"])
def addStu():
    if g.Turntable:
        data = request.get_json()["data"]
        intoStudentInfo(database, data["id"], data["name"], data["sex"], data["age"], data["address"])
        return jsonify({"code": True}), 200
    else:
        return jsonify({"code": False, "msg": "请先登录"})


if __name__ == '__main__':
    app.run()
