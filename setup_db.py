import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def create_user_table(conn):
    """Create user table."""
    cur = conn.cursor()
    try:
        sql = ("CREATE TABLE users ("
               "userid INTEGER NOT NULL,"
               "username VARCHAR(20) NOT NULL,"
               "firstname VARCHAR(40) NOT NULL,"
               "lastname VARCHAR(40) NOT NULL,"
               "email VARCHAR(40) NOT NULL,"
               "passwordhash VARCHAR(120) NOT NULL,"
               "role TEXT, "
               "PRIMARY KEY(userid),"
               "UNIQUE(username) )"
               )
        cur.execute(sql)
        conn.commit
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    else:
        print("Table created.")
    finally:
        cur.close()


def create_activity_table(conn):
    """Create activity table."""
    cur = conn.cursor()
    try:
        sql = ("CREATE TABLE activities ("
               "activity_id INTEGER PRIMARY KEY NOT NULL,"
               "username VARCHAR(20) NOT NULL,"
               "title VARCHAR(40) NOT NULL,"
               "date DATE NOT NULL,"
               "location VARCHAR(40) NOT NULL,"
               "description TEXT NOT NULL,"
               "image TEXT,"
               "created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
               "FOREIGN KEY(username) REFERENCES users(username) ON DELETE CASCADE,"
               "FOREIGN KEY(image) REFERENCES images(fpath) ON DELETE CASCADE )"
               )
        cur.execute(sql)
        conn.commit
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    else:
        print("Table created.")
    finally:
        cur.close()



def create_participation_table(conn):
    """Create participation table."""
    cur = conn.cursor()
    try:
        sql = ("CREATE TABLE participations ("
               "username VARCHAR(20) NOT NULL, "
               "activity_id INTEGER NOT NULL,"
               "since TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
               "FOREIGN KEY(username) REFERENCES users(username) ON DELETE CASCADE,"
               "FOREIGN KEY(activity_id) REFERENCES activities(activity_id) ON DELETE CASCADE ,"
               "UNIQUE(username, activity_id) ON CONFLICT IGNORE )"
        )
        cur.execute(sql)
        conn.commit
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    else:
        print("Table created.")
    finally:
        cur.close()



# add user
def add_user(conn, username, firstname, lastname, email, passwordhash, role):
    """Add user. Returns the new user id"""
    cur = conn.cursor()
    try:
        sql = ("INSERT INTO users (username, firstname, lastname, email, passwordhash, role) VALUES (?,?,?,?,?,?)")
        cur.execute(sql, (username, firstname, lastname, email, passwordhash, role))
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return -1
    else:
        print("User {} created with id {}.".format(username, cur.lastrowid))
        return cur.lastrowid
    finally:
        cur.close()


# add new activity
def add_new_activity(conn, username, title, date, location, description, image):
    """Add new activity. Returns the new activity_id"""
    cur = conn.cursor()
    try:
        sql = ("INSERT INTO activities (username, title, date, location, description, image) VALUES (?,?,?,?,?,?)")
        cur.execute(sql, (username, title, date, location,  description, image))
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return -1
    else:
        print("Activity {} added with id {}.".format(title, cur.lastrowid))
        return cur.lastrowid
    finally:
        cur.close()


# add new image
def add_new_image(conn, fpath, activity_id):
    """Add new image. Returns the new image_id"""
    cur = conn.cursor()
    try:
        sql = ("INSERT INTO images (fpath, activity_id) VALUES (?,?)")
        cur.execute(sql, (fpath, activity_id))
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return -1
    else:
        print("Image {} added with image_id {}.".format(fpath, cur.lastrowid))
        return cur.lastrowid
    finally:
        cur.close()


# add participation
def add_new_pacticipation(conn, username, activity_id):
    """Add participation"""
    cur = conn.cursor()
    try:
        sql = ("INSERT INTO participations(username, activity_id) VALUES (?,?)")
        cur.execute(sql, (username, activity_id))
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return -1
    else:
        print("User {} participate in the activity {}.".format(username, activity_id))
        return cur.lastrowid
    finally:
        cur.close()


# update activity
def update_activity(conn,  activity_id, title, date, location, description):
    """Update activity"""
    cur = conn.cursor()
    try:
        sql = ("UPDATE activities SET "
                "title=?, date=?, location=?, description=?"
                "WHERE activity_id = ?")
        cur.execute(sql, (title, date, location, description, activity_id))
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return 0
    else:
        print("Updates {} activity.".format(cur.rowcount))
        return cur.rowcount
    finally:
        cur.close()


# delete activity
def delete_activity(conn, activity_id):
    """Delete activity."""
    cur = conn.cursor()
    try:
        sql = ("DELETE FROM activities WHERE activity_id = ?")
        cur.execute(sql, (activity_id,))
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return 0
    else:
        print("Removed activity with id {}.".format(cur.rowcount))
        return cur.rowcount
    finally:
        cur.close()


# get all activites (ordered by created)
def get_all_activities(conn):
    """Get all activites (ordered by created)"""
    cur = conn.cursor()
    try:
        sql = (
            "SELECT username, activity_id, title, date, location, description, image,"
            "(SELECT COUNT(*) FROM participations WHERE participations.activity_id = activities.activity_id) AS participants,"
            "created FROM activities WHERE DATE(date) >= DATE() ORDER BY created DESC"
        )
        cur.execute(sql)
        activities = []
        for row in cur:
            (username, activity_id, title, date, location, description, image, participants, created) = row
            activities.append({
                "username": username,
                "activity_id": activity_id,
                "title": title,
                "date": date,
                "location": location,
                "description": description,
                "image": image,
                "participants": participants,
                "created": created,
            })
        return activities
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()

# get all activites (ordered by date)
def get_all_activities_date(conn):
    """Get all activites (ordered by date)"""
    cur = conn.cursor()
    try:
        sql = (
            "SELECT username, activity_id, title, date, location, description, image,"
            "(SELECT COUNT(*) FROM participations WHERE participations.activity_id = activities.activity_id) AS participants,"
            "created FROM activities WHERE DATE(date) >= DATE() ORDER BY date"
        )
        cur.execute(sql)
        activities = []
        for row in cur:
            (username, activity_id, title, date, location, description, image, participants, created) = row
            activities.append({
                "username": username,
                "activity_id": activity_id,
                "title": title,
                "date": date,
                "location": location,
                "description": description,
                "image": image,
                "participants": participants,
                "created": created,
            })
        return activities
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()



# get activites created by user
def get_activities_by_username(conn, username):
    """Get all activites by username"""
    cur = conn.cursor()
    try:
        sql = ("SELECT username, activity_id, title, date, location, description, image,"
        "(SELECT COUNT(*) FROM participations WHERE participations.activity_id = activities.activity_id) AS participants,"
        "created FROM activities WHERE username = ?")
        cur.execute(sql, (username,))
        activities = []
        for row in cur:
            (username, activity_id, title, date, location, description, image, participants, created) = row
            activities.append({
                "username": username,
                "activity_id": activity_id,
                "title": title,
                "date": date,
                "location": location,
                "description": description,
                "image": image,
                "participants": participants,
                "created": created,
            })
        return activities
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()

# get activites that the user will participate in
def get_activities_user_participation(conn, username):
    """Get all activites that the user is signed up for"""
    cur = conn.cursor()
    try:
        sql = ("SELECT a.username, p.activity_id, a.title, a.date, a.location, a.description, a.image,"
                " (SELECT COUNT(*) FROM participations WHERE a.activity_id = participations.activity_id) AS participants, a.created"
                " FROM activities a"
                " LEFT JOIN participations p"
                " ON a.activity_id = p.activity_id"
                " WHERE p.username = ? OR a.username = ?")
        cur.execute(sql, (username, username))
        activities = []
        for row in cur:
            (username, activity_id, title, date, location, description, image, participants, created) = row
            activities.append({
                "username": username,
                "activity_id": activity_id,
                "title": title,
                "date": date,
                "location": location,
                "description": description,
                "image": image,
                "participants": participants,
                "created": created,
            })
        print("PARTICIPATION", activities)
        return activities
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()

# get user acitvities
def get_user_activities(conn, userid):
    """Get user details by name."""
    cur = conn.cursor()
    try:
        sql = ("SELECT activity_id, title, date, location, description, image FROM activities WHERE userid = ?")
        cur.execute(sql, (userid,))
        activities = []
        for row in cur:
            (activity_id, title, date, location, description, image) = row
            activities.append({
                "activity_id": activity_id,
                "title": title,
                "date": date,
                "location": location,
                "description": description,
                "image": image
            })
        return activities
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()

# get user by name
def get_user_by_name(conn, username):
    """Get user details by name."""
    cur = conn.cursor()
    try:
        sql = ("SELECT userid, username, firstname, lastname FROM users WHERE username = ?")
        cur.execute(sql, (username,))
        for row in cur:
            (userid, username, firstname, lastname) = row
            return {
                "userid": userid,
                "username": username,
                "firstname": firstname,
                "lastname": lastname
            }
        else:
            # if user does not exist
            return {
                "userid": None,
                "username": None,
                "firstname": None,
                "lastname": None
            }
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()

# get user by id
def get_user_by_id(conn, userid):
    """Get user details by id."""
    cur = conn.cursor()
    try:
        sql = ("SELECT userid, username, firstname, lastname FROM users WHERE userid = ?")
        cur.execute(sql, (userid,))
        for row in cur:
            (userid, username, firstname, lastname) = row
            return {
                "userid": userid,
                "username": username,
                "firstname": firstname,
                "lastname": lastname
            }
        else:
            #if user does not exist
            return {
                "userid": None,
                "username": None,
                "firstname": None,
                "lastname": None
            }
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()

# get hash for login
def get_hash_for_login(conn, username):
    """Get user details from id."""
    cur = conn.cursor()
    try:
        sql = ("SELECT passwordhash FROM users WHERE username=?")
        cur.execute(sql, (username,))
        for row in cur:
            (passhash,) = row
            return passhash
        else:
            return None
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()

#return a image from an activity
def get_activity_image(conn, activity_id):
    """Get user details by id."""
    cur = conn.cursor()
    try:
        sql = ("SELECT fpath FROM images WHERE activity_id = ?")
        cur.execute(sql, (activity_id,))
        for row in cur:
            (fpath,) = row
            return fpath
        else:
            #if image does not exist
            return None
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()


# get all activites
def get_all_images(conn):
    """Get all images"""
    cur = conn.cursor()
    try:
        sql = ("SELECT fpath, activity_id FROM images")
        cur.execute(sql)
        images = []
        for row in cur:
            (fpath, activity_id) = row
            images.append({
                "fpath": fpath,
                "activity_id": activity_id,
            })
        return images
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()




if __name__ == "__main__":
    try:
        conn = sqlite3.connect("database.db")
    except sqlite3.Error as err:
        print(err)
    else:
        # create user, activity and participation table:
        create_user_table(conn)
        create_activity_table(conn)
        create_participation_table(conn)


        # example user data:
        add_user(conn, "aase", "Åse", "Sagebakken", "aase@hotmail.com", generate_password_hash("passord"), "user")
        add_user(conn, "jorgen", "Jørgen", "Johannessen", "jorgen@hotmail.com", generate_password_hash("passord"), "user")
        add_user(conn, "maribj", "Mari", "Bjordal", "mari@gmail.com", generate_password_hash("passord"), "user")
        add_user(conn, "livesa", "Live", "Sagebakken", "live@hotmail.com", generate_password_hash("passord"), "user")
        add_user(conn, "lenala", "Lena", "Lundervold", "lena@hotmail.com", generate_password_hash("passord"), "user")

        
        # add new activities:
        add_new_activity(conn, "aase", "Joggetur rundt Mosvannet",  "2021-12-15", "Stavanger", "Bli med på en rolig joggetur rundt Mosvannet.\n\nStarter kl 10 om morgenen.", "jogge.jpg")
        add_new_activity(conn, "maribj", "Tur til Preikestolen",  "2021-12-16", "Preikestolen", "SIS arrangerer tur til Preikestolen.\n\nMer informasjon kommer!", "preikestolen.jpg")
        add_new_activity(conn, "livesa", "Digital Paint'n Sip",  "2021-12-15", "Digitalt", "DIGITAL PAINT'N SIP \n\n Har du lyst til å bli med på Paint'n Sip den 15.desember? \n Meld deg på! \n\n Du får tilsendt maling og lerret.", "paintnsip.png")
        add_new_activity(conn, "jorgen", "Grilling",  "2022-06-06", "Godalen", "Grilling ved Godalen", "grill.jpg")


        add_new_pacticipation(conn, "aase", 2)

        # test get_user_by_id and get_user_by_name:
        print("USER", get_user_by_id(conn, 1))
        print("USER", get_user_by_name(conn, "maribj"))

        # test get_hash_for_login:
        hash = get_hash_for_login(conn, "maribj")
        print("Check password: {}".format(check_password_hash(hash,"passord")))

        # close connection to database
        conn.close()
