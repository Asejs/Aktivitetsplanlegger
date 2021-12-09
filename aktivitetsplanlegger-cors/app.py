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
from flask import send_from_directory
from flask_session import Session

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
    response.headers['Access-Control-Allow-Headers'] = "Content-Type, Accept, Content-Length, Authorization"
    return response
app.config['CORS_HEADERS'] = 'Content-Type'
# Upload folder
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)


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
@app.route("/register", methods=["POST"])
def register():
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

# Get activity image:
@app.route("/activity_image_get", methods=["GET"])
def get_activity_image():
    conn = get_db()
    activity_image = get_activity_image(conn)
    return json.dumps(activity_image)

# Get all activities:
@app.route("/images_get", methods=["GET"])
def get_images():
    conn = get_db()
    activities = get_all_images(conn)
    return json.dumps(activities)

# Add activity:
@app.route("/add_activity_post", methods=["POST"])
def add_activity_post():
    #session.pop('activity_id', None)
    newactivity = request.get_json()
    print("get json", request.get_json())
    conn = get_db()
    session['activity_id']  = add_new_activity(conn, newactivity["username"], newactivity["title"], newactivity["date"], newactivity["location"], newactivity["description"])
    print(session["activity_id"])
    return ""


# Set activity:
@app.route("/activities/<activity_id>", methods=["PUT"])
def set_activity(activity_id):
    session.pop('activity_id', None)
    userid = session.get("userid", None)
    if userid == None:
        abort(404)
    activity_id = session.get("activity_id", None)
    if activity_id == None:
        abort(404)
    activity = request.get_json()


    if len(activity.get("title", "")) == 0 or activity.get("activity_id", "-1") != activity_id:
        abort(400)
    conn = get_db()
    affected = update_activity(conn, activity, userid)

    if affected == 0:
        abort(400)

    session['activity_id'] = add_new_activity(conn, activity, userid)
    print(session["activity"])
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



# ----- BILDEOPPLASTNING -----

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#needed for accessing pictures in the uploads-folder
@app.route('/uploads/<filename>', methods=['GET', 'POST'])
def display_image(filename):
    print('filename: ' + filename)    
    return send_from_directory(app.config.get('UPLOAD_FOLDER'), filename)

#this functions checks if the filname exists in either the filesystem or in the database and resolves the name-conflict
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
        if 'file' not in request.files:
            print('No file part')
            return ''
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return ''
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            folder, ext = os.path.splitext(filename)
            print("folder:", folder, ". ext:", ext)
            #filename = resolve_file_conflict(app.config.get('UPLOAD_FOLDER'), filename)

            conn = get_db()
            print("SESSION BEFORE", session)
            image = add_new_image(conn, filename, session.get('activity_id'))

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return {"publish": "success"}

'''
#needed for accessing pictures in the uploads-folder
@app.get('/image/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config.get('UPLOAD_FOLDER'), filename)



#this functions checks if the filname exists in either the filesystem or in the database and resolves the name-conflict
def resolve_file_conflict(folder, filename):
    name, extension = os.path.splitext(filename)
    n = 0
    while os.path.exists(os.path.join(folder, filename)) or check_img(get_db(), filename):
        n += 1
        filename = '%s_%d%s' % (name, n, extension)
    return filename

#this function takes an input file and folder and resizes the image provided to the width set in the config
#the new dimensions of the image is appended to the filename
#if the original width is less than the configured width, the image is kept as is.
def resize_image(folder, filename, new_width):
    path = os.path.join(folder, filename)
    image = cv2.imread(path)
    old_width = int(image.shape[1])
    if old_width <= new_width:
        return filename, None
    ratio = new_width / old_width
    new_height = int(image.shape[0]) * ratio
    dim = (int(new_width), int(new_height))
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    name, extension = os.path.splitext(filename)
    resolution = '%dX%d' %(new_width, new_height)
    filename = '%s_%s%s' % (name, resolution, extension)
    filename = resolve_file_conflict(folder, filename)
    return filename, resized

'''


if __name__ == "__main__":
    app.run(debug=True)