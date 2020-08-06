from app import app
from flask import redirect, render_template, request, session

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    # TODO: check username and password
    session["username"] = username
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/testi1")
def testi1():
    return render_template("testi1.html")

@app.route("/testi2")
def testi2():
    return render_template("testi2.html")

@app.route("/tulokset")
def tulokset():
    return render_template("tulokset.html")