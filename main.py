from flask import Flask, escape, request, g
from flask import render_template, make_response
import sqlite3
import json
import time
import service
import sendemail
from threading import Thread, Timer

app = Flask(__name__)

ctx = app.app_context()

DATABASE = './database.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


ctx.push()
# create table
conn = get_db()
conn.execute(
    "CREATE TABLE if not exists user"
    "(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user varchar(32) UNIQUE,"
    "password varchar(32), email varchar(32), area varchar(160))")
conn.commit()


def timer():
    with app.app_context():
        while True:
            time.sleep(0.8)
            t = time.localtime(time.time())
            if (t.tm_hour == 12 and t.tm_min == 6 and t.tm_sec == 11):
                conn = get_db()
                cur = conn.execute("SELECT * FROM user")
                for user in cur.fetchall():
                    u = user[1]
                    password = user[2]
                    email = user[3]
                    area = user[4]
                    # 执行签到
                    rs = service.do_signin(u, password, area)
                    # 发送邮件
                    now = time.strftime("%Y-%m-%d,%H:%M", time.localtime())
                    day = str(t.tm_mon) + "月" + str(t.tm_mday) + "日"
                    if rs == True:
                        sendemail.send_email(
                            day + "签到成功提示", "您的帐号`" + u + "`在" + now + "签到成功", email)
                    else:
                        sendemail.send_email(
                            day + "自动签到失败提示", "您的帐号`" + u + "`签到失败，请登录APP客户端手动签到", email)


tt = Thread(target=timer)
tt.start()
ctx.pop()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.route("/")
@app.route("/index.html")
def home():
    resp = make_response(render_template("index.html"))
    resp.set_cookie("quanye", "Love you!")
    return resp


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/tools")
def tools():
    return render_template("tools.html")


@app.route("/tools/signin")
def signin():
    return render_template("tools/signin.html")


@app.route("/tools/service/addSigner", methods=["POST"])
def addSigner():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    user = json_data.get("user")
    password = json_data.get("password")
    email = json_data.get("email")
    area = json_data.get("area")

    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute(
            "insert into user(user, password, email, area) values (?, ?, ?, ?)", (user, password, email, area))
        conn.commit()
        return "添加成功"
    except sqlite3.IntegrityError:
        return "该用户名已经添加过了，不需要重新添加"
