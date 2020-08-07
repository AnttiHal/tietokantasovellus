from app import app
from flask import redirect, render_template, request, session
import users

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["get","post"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username,password):
            return redirect("/")
        else:
            return render_template("error.html",message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["get","post"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        if users.register(username,password):
            return redirect("/")
        else:
            return render_template("error.html",message="Rekisteröinti ei onnistunut")

@app.route("/testi1")
def testi1():
    return render_template("testi1.html")

@app.route("/testi2")
def testi2():
    return render_template("testi2.html")

@app.route("/tulokset")
def tulokset():
    return render_template("tulokset.html")