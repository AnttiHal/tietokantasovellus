from app import app
from flask import redirect, render_template, request, session
import users
from db import db 

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
    if 'username' in session:
        del session["username"]
    if 'user_id' in session:
        del session["user_id"]
    if 'admin' in session:
        del session["admin"]
    return redirect("/")

@app.route("/register", methods=["get","post"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]
        
        if len(username) > 20:
            return render_template("error.html", message="Käyttäjätunnus on liian pitkä")
        if len(password) > 20:
            return render_template("error.html", message="Salasana on liian pitkä")

        if users.register(username,password,role):
            return redirect("/")
        elif role == "":
            return render_template("error.html", message="et valinnut käyttäjälle roolia")
        elif password == "":
            return render_template("error.html",message="Salasana-kenttä ei voi olla tyhjä")
        elif username == "":
            return render_template("error.html",message="Tunnus-kenttä ei voi olla tyhjä")
        

        else:
            return render_template("error.html",message="Rekisteröinti ei onnistunut")

@app.route("/kuuntelu")
def kuuntelu():
    sql = "SELECT id, topic, created_at FROM tests WHERE type=2"
    result = db.session.execute(sql)
    tests = result.fetchall()
    return render_template("kuuntelu.html", tests=tests)

@app.route("/tunnistus")
def tunnistus():

    sql = "SELECT id, topic, created_at FROM tests WHERE type=1"
    result = db.session.execute(sql)
    tests = result.fetchall()
    return render_template("tunnistus.html", tests=tests)



@app.route("/newtest")
def newtest():
    return render_template("newtest.html")

@app.route("/newtest-basic")
def newtest_basic():
    return render_template("newtest-basic.html")



@app.route("/create-basic", methods=["POST"])
def create_basic():
    topic = request.form["topic"]
    sql = "INSERT INTO tests (topic, created_at, type) VALUES (:topic, NOW(), 1) RETURNING id"
    result = db.session.execute(sql, {"topic":topic})
    test_id = result.fetchone()[0]
    notes = request.form.getlist("note")
    for note in notes:
        if note != "":
            sql = "INSERT INTO notes (test_id, note) VALUES (:test_id, :note)"
            db.session.execute(sql, {"test_id":test_id, "note":note})

    choices = request.form.getlist("choice")
    for choice in choices:
        if choice != "":
            sql = "INSERT INTO choices (test_id, choice) VALUES (:test_id, :choice)"
            db.session.execute(sql, {"test_id":test_id, "choice":choice})
    answer = request.form["answer"]    
    sql = "INSERT INTO right_answers (test_id, answer) VALUES (:test_id, :answer)"
    db.session.execute(sql, {"test_id":test_id, "answer":answer})
    db.session.commit()
    return render_template("message.html", message="Uusi tunnistustesti luotu")

@app.route("/create", methods=["POST"])
def create():
    topic = request.form["topic"]
    sql = "INSERT INTO tests (topic, created_at, type) VALUES (:topic, NOW(), 2) RETURNING id"
    result = db.session.execute(sql, {"topic":topic})
    test_id = result.fetchone()[0]
    audio_url = request.form["audio_url"]
    sql = "INSERT INTO audios (audio_url, test_id) VALUES (:audio_url, :test_id)"
    db.session.execute(sql, {"audio_url":audio_url, "test_id":test_id})
    answer = request.form["answer"]
    
    sql = "INSERT INTO right_answers (test_id, answer) VALUES (:test_id, :answer)"
    db.session.execute(sql, {"test_id":test_id, "answer":answer})
    db.session.commit()
    return render_template("message.html", message="Uusi kuuntelutesti luotu")


@app.route("/audiotest/<int:id>")
def audiotest(id):
    sql = "SELECT topic FROM tests WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    topic = result.fetchone()[0]
    sql = "SELECT audio_url FROM audios WHERE test_id=:id"
    result = db.session.execute(sql, {"id":id})
    audio_url = result.fetchone()[0]
    return render_template("audiotest.html", id=id, topic=topic, audio_url=audio_url)

@app.route("/basictest/<int:id>")
def basictest(id):
    sql = "SELECT topic FROM tests WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    topic = result.fetchone()[0]
    sql = "SELECT id, note FROM notes WHERE test_id=:id"
    result = db.session.execute(sql, {"id":id})
    notes = result.fetchall()
    sql = "SELECT id, choice FROM choices WHERE test_id=:id"
    result = db.session.execute(sql, {"id":id})
    choices = result.fetchall()
    return render_template("basictest.html", id=id, topic=topic, choices=choices, notes=notes)


@app.route("/answer", methods=["POST"])
def answer():
    test_id = request.form["id"]
    user_id = users.user_id()
    if "answer" in request.form:
        
        answer = request.form["answer"]
        sql = "INSERT INTO answers (answer, test_id, user_id) VALUES (:answer, :test_id, :user_id)"
        db.session.execute(sql, {"test_id":test_id, "answer":answer, "user_id":user_id})
        db.session.commit()
    return redirect("/result/"+str(test_id))



@app.route("/result/<int:id>")
def result(id):
    sql = "SELECT type FROM tests WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    page = result.fetchone()[0]
    user_id = users.user_id()
    sql = "SELECT topic FROM tests WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    topic = result.fetchone()[0]
    sql = "SELECT answer FROM right_answers WHERE test_id=:test_id"
    result = db.session.execute(sql,{"test_id":id})
    right_answer = result.fetchone()[0]
    sql = "SELECT answer FROM answers WHERE test_id=:test_id and user_id=:user_id order by id desc"
    result = db.session.execute(sql,{"test_id":id, "user_id":user_id})
    answer = result.fetchone()[0]
    correct = False
    if answer == right_answer:
        correct = True
    
    return render_template("result.html", topic=topic, right_answer=right_answer, answer=answer, correct=correct, page=page)


@app.route("/tilastot")
def tilastot():
    sql = "SELECT id, username FROM users WHERE role=1"
    result = db.session.execute(sql)
    admins = result.fetchall()

    sql = "SELECT id, username FROM users WHERE role=0"
    result = db.session.execute(sql)
    users = result.fetchall()

    sql = "SELECT count(*) FROM answers"
    result = db.session.execute(sql)
    count_answer = result.fetchone()[0]

    sql = "SELECT count(*) FROM tests"
    result = db.session.execute(sql)
    count_tests = result.fetchone()[0]

    sql = "SELECT count(*) FROM tests WHERE type=2"
    result = db.session.execute(sql)
    count_audiotests = result.fetchone()[0]

    sql = "SELECT count(*) FROM tests WHERE type=1"
    result = db.session.execute(sql)
    count_basictests = result.fetchone()[0]

    return render_template("tilastot.html", users=users, admins=admins, count_answer=count_answer, count_tests=
    count_tests, count_audiotests=count_audiotests, count_basictests=count_basictests)

@app.route("/tilastot/<string:username>")
def opiskelija_tilastot(username):
    
    sql = "SELECT id, username FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()[1]

    sql = "SELECT t.topic, a.answer, r.answer FROM users u, tests t, answers a, right_answers r WHERE username=:username AND t.id=a.test_id AND a.user_id=u.id AND r.test_id=t.id"
    result = db.session.execute(sql, {"username":username})
    answers = result.fetchall()

    sql = "SELECT count(*) FROM answers a, right_answers r, users u WHERE r.test_id=a.test_id AND  u.username=:username AND a.answer=r.answer AND a.user_id=u.id"
    result = db.session.execute(sql, {"username":username})
    right_answers_count = result.fetchone()[0]

    sql = "SELECT count(*) FROM answers a , users u WHERE username=:username AND a.user_id=u.id"
    result = db.session.execute(sql, {"username":username})
    count_answer = result.fetchone()[0]
    
    return render_template("opiskelijatilasto.html", user=user, answers=answers, count_answer=count_answer, right_answers_count=right_answers_count)

@app.route("/tulokset")
def tulokset():
    user_id = users.user_id()

    sql = "SELECT count(*) FROM answers WHERE  user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    answers_count = result.fetchone()[0]

    sql = "SELECT count(*) FROM answers a, right_answers r, tests t WHERE t.id=a.test_id AND t.id=r.test_id AND a.user_id=:user_id AND a.answer=r.answer"
    result = db.session.execute(sql, {"user_id":user_id})
    right_answers_count = result.fetchone()[0]

    sql = "SELECT t.topic, a.answer, r.answer FROM tests t, answers a, right_answers r WHERE t.id=a.test_id AND a.user_id=:user_id AND t.id=r.test_id AND t.type=2"
    result = db.session.execute(sql, {"user_id":user_id})
    results = result.fetchall()

    sql = "SELECT t.topic, a.answer, r.answer FROM tests t, answers a, right_answers r WHERE t.id=a.test_id AND a.user_id=:user_id AND t.id=r.test_id AND t.type=1"
    result = db.session.execute(sql, {"user_id":user_id})
    basicresults = result.fetchall()
    return render_template("tulokset.html", results=results, basicresults=basicresults, answers_count=answers_count, right_answers_count=right_answers_count)




    