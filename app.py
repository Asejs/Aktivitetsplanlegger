from setup_db import *
from flask import Flask, request, redirect, url_for, flash, session, g, abort, jsonify

from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from flask_cors import CORS, cross_origin
import json
import os
from flask import Flask, render_template, send_from_directory, make_response
from werkzeug.utils import secure_filename
from flask import send_from_directory
import datetime


app = Flask(__name__)

app.config.update(
    SESSION_COOKIE_SAMESITE='Strict',
    SESSION_COOKIE_HTTPONLY=True,
    PERMANENT_SESSION_LIFETIME=datetime.timedelta(minutes=1440),
)

# Allow cross-origin requests (CORS)
CORS(app)

# Secret key for session
app.secret_key = 'A213FB1557589757D5ACEED'
app.config["SECRET_KEY"] = "OCML3BRawWEUeaxcuKHLpw"


# Add headers to use sessions on cross-origin requests
@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:8080'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = "PUT,POST,GET,DELETE,OPTIONS"
    response.headers['Access-Control-Allow-Headers'] = "Content-Type, Accept, Content-Length, Authorization"
    return response

app.config['CORS_HEADERS'] = 'Content-Type'

# Upload folder
UPLOAD_FOLDER = "aktivitetsplanlegger-cli/src/assets/uploads"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
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


# Check if login is valid
def valid_login(username, password):
    """Checks if username-password combination is valid."""
    conn = get_db()
    hash = get_hash_for_login(conn, username)
    if hash != None:
        return check_password_hash(hash, password)
    return False


# Login
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not valid_login(data.get("username"), data.get("password")):
        abort(404)
    conn = get_db()
    user = get_user_by_name(conn, data["username"])
    return user


# Logout
@app.route("/logout")
def logout():
    #session.clear()
    print("logged out")
    if "username" in session:
        del session["username"]
    return ""


# returns userid if user exists
def check_user(conn, username):
    user = conn.execute(
            'SELECT userid FROM users WHERE username = ?',
            (username,)
            ).fetchone()
    if user:
        return user[0]
    return None


# Registrer ny bruker
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    hash = generate_password_hash(data["password"])
    conn = get_db()
    if not check_user(conn, data["username"]):
        user = add_user(conn, data["username"], data["firstname"], data["lastname"], data["email"], hash, "user")
        print("user", user)
        session["username"] = data["username"]
        return {'register': "success"}
    return {
        'register': 'failed',
        'error': 'Username is already taken'
    }


# Get user
@app.route("/user", methods=["GET"])
def get_user(username):
    if username == None:
        abort(404)
    conn = get_db()
    user = get_user_by_name(conn, username)
    return user


# Get activities
@app.route("/activities_get", methods=["GET"])
def get_activities():
    conn = get_db()
    activities = get_all_activities(conn)
    return json.dumps(activities)

# Get activities (order by date)
@app.route("/activities_get_date", methods=["GET"])
def get_activities_date():
    conn = get_db()
    activities = get_all_activities_date(conn)
    return json.dumps(activities)

# Get activities created by username
@app.route("/activities_get_by_username/<username>", methods=["GET"])
def get_all_activities_by_username(username):
    print("USERNAME", username)
    conn = get_db()
    activities = get_activities_by_username(conn, username)
    return json.dumps(activities)

# Get activities that the user is signed up for
@app.route("/activities_get_user_participation/<username>", methods=["GET"])
def get_all_activities_user_participation(username):
    conn = get_db()
    activities = get_activities_user_participation(conn, username)
    return json.dumps(activities)


# Add activity
@app.route("/add_activity_post", methods=["POST"])
def add_activity_post():
    #session.pop('activity_id', None)
    newactivity = request.get_json()
    print("get json", request.get_json())
    conn = get_db()
    activity_id = add_new_activity(conn, newactivity["username"], newactivity["title"], newactivity["date"], newactivity["location"], newactivity["description"])
    session.permanent = True
    return ''


# Set activity
@app.route("/set_activity/<activity_id>", methods=["PUT"])
def set_activity(activity_id):
    conn = get_db()
    update_activity(conn, activity_id, request.form['title'], request.form['date'], request.form['location'], request.form['description'])
    return {"edit": "success"}


# Delete activity
@app.route("/del_activities/<activity_id>", methods=["DELETE"])
def del_activity(activity_id):
    conn = get_db()
    affected = delete_activity(conn, activity_id)
    if affected == 0:
        abort(400)
    return ""

# Add participation
@app.route("/participate/<activity_id>", methods=["POST"])
def add_participation(activity_id):
    data = request.get_json()
    conn = get_db()
    add_new_pacticipation(conn, data["username"], activity_id)
    return ""


# BILDEOPPLASTNING

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# needed for accessing pictures in the upload-folder
@app.route('/uploads/<filename>', methods=['GET', 'POST'])
def display_image(filename):
    print('filename: ' + filename)    
    return send_from_directory(app.config.get('UPLOAD_FOLDER'), filename)

# check if the filname exists in either the filesystem or in the database and resolves the name-conflict
def resolve_file_conflict(folder, filename):
    name, extension = os.path.splitext(filename)
    n = 0
    while os.path.exists(os.path.join(folder, filename)) or check_img(get_db(), filename):
        n += 1
        filename = '%s_%d%s' % (name, n, extension)
    return filename


@app.route("/upload_image", methods=['POST', 'GET'])
def upload_image():
    if request.method == 'POST':
        # upload activity
        print("get form", request.form)

        # upload image
        if 'file' not in request.files:
            print('No file part')
            conn = get_db()
            activity_id = add_new_activity(conn, request.form['username'], request.form['title'], request.form['date'], request.form['location'], request.form['description'], request.form['radio'])
            return {"publish": "success"}
        file = request.files['file']

        if file.filename == '':
            print('No selected file')
            return ''
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            folder, ext = os.path.splitext(filename)
            print("folder:", folder, ". ext:", ext)
            # checks for name conflicts on the filesystem and database and resolves them
            filename = resolve_file_conflict(app.config.get('UPLOAD_FOLDER'), filename)
        
        conn = get_db()
        activity_id = add_new_activity(conn, request.form['username'], request.form['title'], request.form['date'], request.form['location'], request.form['description'], filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return {"publish": "success"}


# this functions checks if the filename exists in either the filesystem or in the database and resolves the name-conflict
def resolve_file_conflict(folder, filename):
    name, extension = os.path.splitext(filename)
    n = 0
    while os.path.exists(os.path.join(folder, filename)):
        n += 1
        filename = '%s_%d%s' % (name, n, extension)
    return filename

# checks if the filename exists in the database
def check_img(conn, filename):
    img = conn.execute(
            'SELECT * FROM images'
            ' WHERE fpath = ?',
            (filename)
            ).fetchone()
    if img is not None:
        return True
    return False

if __name__ == "__main__":
    app.run(debug=True)