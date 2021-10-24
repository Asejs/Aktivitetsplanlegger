from setup_db import *
from flask import Flask, request, redirect, url_for, flash, session, g, abort, jsonify
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from flask_cors import CORS, cross_origin
import json
import os
from flask import Flask, render_template, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
# Allow cross-origin requests (CORS)
cors = CORS()

# Secret key for session
app.secret_key = 'A213FB1557589757D5ACEED'

# Add headers to use sessions on cross-origin requests
@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:8080'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = "PUT,POST,GET,DELETE,OPTIONS"
    response.headers['Access-Control-Allow-Headers'] = "Content-Type, Content-Length, Authorization"
    return response

# Upload folder
UPLOAD_FOLDER = '/path/to/the/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Get database
def get_db():
    if not hasattr(g, "_database"):
        print("create connection")
        g._database = sqlite3.connect("database.db")
    return g._database

# Close the database at the end of the request
@app.teardown_appcontext
def teardown_db(error):
    """Closes the database at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        print("close connection")
        db.close()

"""
# Check if there is a loggedin user
@app.route("/userdata", methods=["GET"])
def userdata():
    if session.get("username", None):
        user = get_user()
        return user
    return jsonify("")
"""

# Check if login is valid
def valid_login(username, password):
    """Checks if username-password combination is valid."""
    conn = get_db()
    hash = get_hash_for_login(conn, username)
    if hash != None:
        return check_password_hash(hash, password)
    return False


# Login funksjon som sjekker om det er en valid login og setter en session på brukernavn og rollen til brukeren
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not valid_login(data.get("username", ""), data.get("password", "")):
        abort(404)
    conn = get_db()
    user = get_user_by_name(conn, data["username"])
    # session
    session["userid"] = user["userid"]
    return user

"""
@app.route("/login", methods=["GET", "POST"])
def login():
# if the form was submitted (otherwise we just display form)
    if request.method == "POST":  
        user_form = request.get_json()
        username = user_form["username"]
        password = user_form["password"]
        if valid_login(username, password):
            conn = get_db()
            user = get_user_by_name(conn, username)
            session["username"] = user["username"]
            session["role"] = user["role"]
            return jsonify(user)
        else:
            return jsonify("Feil brukernavn eller passord!")
    return jsonify("")
"""


# Logout
@app.route("/logout")
def logout():
    session.clear()
    print("logged out")
    if "username" in session:
        del session["username"]
    return ""
    
"""
@app.route("/logout", methods=["GET"])
def logout():
    session.pop("username", None)
    session.pop("role", None)
    return jsonify("")
"""

# Register
@app.route("/signup", methods=["POST"])
def signup_post():
    data = request.get_json()
    print(data)
    hash = generate_password_hash(data["password"])
    conn = get_db()
    user = add_user(conn, data["username"], data["firstname"], data["lastname"], data["email"], hash, "admin")
    print("user", user)
    session["username"] = data["username"]
    print(session)
    return ""


# Get user
@app.route("/user", methods=["GET"])
def get_user(username):
    if userid == None:
        abort(404)
    conn = get_db()
    user = get_user_by_name(conn, username)
    return user


# Get activities:
@app.route("/activities_get", methods=["GET"])
def get_activities():
    conn = get_db()
    activities = get_all_activities(conn)
    return json.dumps(activities)


# Add activity:
@app.route("/add_activity_post", methods=["POST"])
def add_activity_post():
    newactivity = request.get_json()
    conn = get_db()
    activity = add_new_activity(conn, newactivity["username"], newactivity["title"], newactivity["date"], newactivity["location"], newactivity["description"])
    return ""


# Set activity:
@app.route("/activities/<activity_id>", methods=["PUT"])
def set_activity(activity_id):
    userid = session.get("userid", None)
    if userid == None:
        abort(404)
    activity = request.get_json()
    if len(activity.get("title", "")) == 0 or activity.get("activity_id", "-1") != activity_id:
        abort(400)
    conn = get_db()
    affected = update_activity(conn, activity, userid)
    if affected == 0:
        abort(400)
    return ""


# Delete activity:
@app.route("/del_activities/<activity_id>", methods=["DELETE"])
def del_activity(activity_id):
    print(activity_id)
    conn = get_db()
    affected = delete_activity(conn, activity_id)
    if affected == 0:
        abort(400)
    return ""




if __name__ == "__main__":
    app.run(debug=True)