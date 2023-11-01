from flask import Flask, request, jsonify
from flask_cors import CORS

from myjwt import set_token, get_token
from web_sqlite import StudentList

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config["JSON_AS_ASCII"] = False


@app.before_request
def my_before_request():  # 路由守卫
    if not request.path == "/login":
        token = request.headers.get("token")
        if token:
            if not get_token(token):
                return jsonify({"code": False, "msg": "token过期请重新登录"})
        else:
            return jsonify({"code": False, "msg": "请先登录"})


@app.route("/getAllStudentInfo", methods=["GET", "POST"])
def get_all_student_info():  # 给前端发送全部学生的基础信息
    datalist = []
    with StudentList() as database:
        data = database.get_all_student_info()
        for i in data:
            datalist.append(dict(zip(["id", "name", "sex", "age", "address"], i)))
    return jsonify(
        {
            "code": True,
            "data": datalist,
            "msg": "获取全部学生基础信息"
        }
    ), 200


@app.route("/getOneStudentInfo", methods=["POST"])
def get_one_student_info():  # 给前端发送单个学生的基础信息
    user = request.get_json()["user"]
    with StudentList() as database:
        return jsonify(
            {
                "code": True,
                "data": database.get_one_student_info(user),
                "msg": "获取单个学生基础信息",
            }
        ), 200


@app.route("/login", methods=["POST"])
def login():  # 判断是否可以登录
    user = request.get_json()["user"]
    password = request.get_json()["password"]
    with StudentList() as database:
        if database.select_password(user, password):
            return jsonify({"code": True, "msg": "登录成功", "token": set_token(user)}), 200
        else:
            return jsonify({"code": False, "msg": "账号密码错误"}), 200


@app.route("/delStudent", methods=["post"])
def delete_student():  # 删除学生
    user = request.get_json()["user"]
    with StudentList() as database:
        if database.delete_student(user):
            return jsonify({"code": True, "msg": "删除成功"}), 200
        else:
            return jsonify({"code": False, "msg": "删除失败"}), 200


@app.route("/upDataStudent", methods=["post"])
def update_student():  # 更新学生基础信息
    data = request.get_json()["data"]
    with StudentList() as database:
        database.update_student(data["id"], data["name"], data["sex"], data["age"], data["address"])
        return jsonify({"code": True, "msg": "更新信息成功"}), 200


@app.route("/changePassword", methods=["post"])
def change_password():  # 修改管理员密码
    user = request.get_json()["user"]
    pad = request.get_json()["password"]
    with StudentList() as database:
        if database.change_password(user, pad):
            return jsonify({"code": True, "msg": "修改成功"}), 200
        else:
            return jsonify({"code": False, "msg": "修改失败"}), 200


@app.route("/addStu", methods=["post"])
def add_student():  # 添加学生
    data = request.get_json()["data"]
    with StudentList() as database:
        if database.into_student_info(data["id"], data["name"], data["sex"], data["age"], data["address"]):
            return jsonify({"code": True, "msg": "写入成功"}), 200
        else:
            return jsonify({"code": False, "msg": "写入失败"}), 200


@app.route("/getAllCourse", methods=["post"])
def get_all_course():  # 给前端发送每个课程的人数
    with StudentList() as database:
        return jsonify(
            {
                "code": True,
                "data": database.get_all_course(),
                "msg": "每个课程的人数"
            }
        ), 200


@app.route("/getAllStudentScore", methods=["post"])
def get_all_student_score():  # 单个课程全部学生的成绩
    user = request.get_json()["user"]
    with StudentList() as database:
        return jsonify(
            {
                "code": True,
                "data": database.get_all_student_score(user)
            }
        ), 200


@app.route("/getOneStudentScore", methods=["post"])
def get_one_student_score():  # 单个学生全部选课成绩
    user = request.get_json()["user"]
    with StudentList() as database:
        return jsonify(
            {
                "code": True,
                "data": database.get_one_student_score(user),
                "msg": "单个学生全部选课成绩",
            }
        ), 200,


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
