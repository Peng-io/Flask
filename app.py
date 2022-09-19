from flask import Flask, request, jsonify
from flask_cors import *

from myjwt import *
from web_sqlite import StudentList

app = Flask(__name__)
CORS(app, supports_credentials=True, resources=r"/*")
app.config["JSON_AS_ASCII"] = False


@app.before_request
def my_before_request():  # 路由守卫
    if not request.path == "/login":
        token = request.headers.get("token")
        if token:
            if not getToKen(token):
                return jsonify({"code": False, "msg": "token过期请重新登录"})
        else:
            return jsonify({"code": False, "msg": "请先登录"})


@app.route("/getAllStudentInfo", methods=["GET", "POST"])
def getAllStudentInfo():  # 给前端发送全部学生的基础信息
    datalist = []
    with StudentList() as database:
        data = database.getAllStudentInfo()
        for i in data:
            datalist.append(dict(zip(["id", "name", "sex", "age", "address"], i)))
    return jsonify({"code": True, "data": datalist, "msg": "获取全部学生基础信息"}), 200


@app.route("/getOneStudentInfo", methods=["POST"])
def getOneStudentInfo():  # 给前端发送单个学生的基础信息
    user = request.get_json()["user"]
    with StudentList() as database:
        return jsonify({"code": True, "data": database.getOneStudentInfo(user), "msg": "获取单个学生基础信息"})


@app.route("/login", methods=["POST"])
def login():  # 判断是否可以登录
    user = request.get_json()["user"]
    password = request.get_json()["password"]
    with StudentList() as database:
        if database.selectPassword(user, password):
            return jsonify({"code": True, "msg": "登录成功", "token": setToKen(user)}), 200
        else:
            return jsonify({"code": False, "msg": "账号密码错误"}), 200


@app.route("/delStudent", methods=["post"])
def delStudent():  # 删除学生（未完成）
    user = request.get_json()["user"]
    with StudentList() as database:
        if database.delStudent(user):
            return jsonify({"code": True}), 200
        else:
            return jsonify({"code": False}), 200


@app.route("/upDataStudent", methods=["post"])
def upDataStudent():  # 更新学生基础信息
    data = request.get_json()["data"]
    with StudentList() as database:
        database.upDataStudentInfo(
            data["id"], data["name"], data["sex"], data["age"], data["address"]
        )
        return jsonify({"code": True, "msg": "更新信息成功"}), 200


@app.route("/changePassword", methods=["post"])
def changePassword():  # 修改管理员密码
    user = request.get_json()["user"]
    pad = request.get_json()["password"]
    with StudentList() as database:
        if database.changePassword(user, pad):
            return jsonify({"code": True, "msg": "修改成功"}), 200
        else:
            return jsonify({"code": False, "msg": "修改失败"}), 200


@app.route("/addStu", methods=["post"])
def addStu():  # 添加学生
    data = request.get_json()["data"]
    with StudentList() as database:
        if database.intoStudentInfo(
                data["id"], data["name"], data["sex"], data["age"], data["address"]
        ):
            return jsonify({"code": True, "msg": "写入成功"}), 200
        else:
            return jsonify({"code": True, "msg": "写入失败"}), 200


@app.route("/getAllCourse", methods=["post"])
def getAllCourse():  # 给前端发送每个课程的人数
    with StudentList() as database:
        return (
            jsonify({"code": True, "data": database.getAllCourse(), "msg": "每个课程的人数"}),
            200,
        )


@app.route("/getAllStudentScore", methods=["post"])
def getAllStudentScore():  # 未完成 单个课程全部学生的成绩
    data = list()
    with StudentList() as database:
        for i in database.getAllStudentScore():
            data.append(dict(zip(["id", "curriculum_id", "gradeNumber"], i)))
    return jsonify({"code": True, "data": data, }), 200


@app.route("/getOneStudentScore", methods=["post"])
def getOneStudentScore():  # 单个学生全部选课成绩
    user = request.get_json()["user"]
    with StudentList() as database:
        return (
            jsonify(
                {
                    "code": True,
                    "data": database.getOneStudentScore(user),
                    "msg": "",
                }
            ),
            200,
        )


if __name__ == "__main__":
    app.run(host='0.0.0.0')
