from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
import os

def login(username,password):
    sql = "SELECT password, id, role FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return False
    
    else:
        if check_password_hash(user[0],password):
            session["user_id"] = user[1]
            session["username"] = username 
            session["csrf_token"] = os.urandom(16).hex()           
            if user[2] == 1:
                session["admin"] = True
            return  True
        else:
            return False

def logout():
    if 'username' in session:
        del session["username"]
    if 'user_id' in session:
        del session["user_id"]
    if 'admin' in session:
        del session["admin"]

def register(username,password,role):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password, role) VALUES (:username,:password,:role)"
        db.session.execute(sql, {"username":username,"password":hash_value, "role":role})
        db.session.commit()
    except:
        return False
    return login(username,password)

def user_id():
    return session.get("user_id",0)