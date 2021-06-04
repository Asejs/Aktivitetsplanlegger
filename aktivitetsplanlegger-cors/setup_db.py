import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def create_user_table(conn):
    """Create table."""
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
    """Create table."""
    cur = conn.cursor()
    try:
        sql = ("CREATE TABLE activities ("
               "activity_id INTEGER NOT NULL,"
               "username INTEGER NOT NULL,"
               "title VARCHAR(40) NOT NULL,"
               "date DATE NOT NULL,"
               "location VARCHAR(40) NOT NULL,"
               "description TEXT NOT NULL,"
               "PRIMARY KEY(activity_id),"
               "FOREIGN KEY(username) REFERENCES users(username) )"
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
    """Create table."""
    cur = conn.cursor()
    try:
        sql = ("CREATE TABLE participation ("
               "userid INTEGER NOT NULL, "
               "activity_id INTEGER NOT NULL )"
        )
        cur.execute(sql)
        conn.commit
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    else:
        print("Table created.")
    finally:
        cur.close()


# -----------------------------------------------------


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
'''
try:
                # ... Collecting form info ...

                cur.execute("SELECT * FROM users WHERE name = ?", (username))

                if cur.fetchone() is not None:
                    flash("That username is already taken...")
                    return render_template('register.html')
                else:
                    cur.execute("INSERT INTO users (name,password,email) VALUES (?,?,?)",(username,passwordencr,email) )
                    con.commit()
                    flash (...)
             except:
                 con.rollback()

             finally:
                 session['logged_in'] = True
                 session['username'] = username
                 # ... mailing code ...
'''


def add_new_activity(conn, username, title, date, location, description):
    """Add activity. Returns the new activity_id"""
    cur = conn.cursor()
    try:
        sql = ("INSERT INTO activities (username, title, date, location, description) VALUES (?,?,?,?,?)")
        cur.execute(sql, (username, title, date, location,  description))
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return -1
    else:
        print("Activity {} added with id {}.".format(title, cur.lastrowid))
        return cur.lastrowid
    finally:
        cur.close()

def add_new_pacticipation(conn, userid, activity_id):
    """Add particiapation"""
    cur = conn.cursor()
    try:
        sql = ("INSERT INTO participation(userid, activity_id) VALUES (?,?)")
        cur.execute(sql, (userid, activity_id))
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return -1
    else:
        print("User {} participate in the activity {}.".format(userid, cur.lastrowid))
        return cur.lastrowid
    finally:
        cur.close()


def update_activity(conn, activity, userid):
    """Update activity"""
    cur = conn.cursor()
    try:
        sql = ("UPDATE activities SET "
                "title=?, date=?, location=?, description=?"
                "WHERE activity_id = ? AND userid = ?")
        cur.execute(sql, (activity["title"],
                        activity.get("date",None), 
                        activity.get("location",None),
                        activity.get("description",None), 
                        userid))
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return 0
    else:
        print("Updates {} activities.".format(cur.rowcount))
        return cur.rowcount
    finally:
        cur.close()


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


# Get all activites
def get_all_activities(conn):
    """Get all activites"""
    cur = conn.cursor()
    try:
        sql = ("SELECT username, activity_id, title, date, location, description FROM activities")
        cur.execute(sql)
        activities = []
        for row in cur:
            (username, activity_id, title, date, location, description) = row
            activities.append({
                "username": username,
                "activity_id": activity_id,
                "title": title,
                "date": date,
                "location": location,
                "description": description
            })
        return activities
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()


def get_user_activities(conn, userid):
    """Get user details by name."""
    cur = conn.cursor()
    try:
        sql = ("SELECT activity_id, title, date, location, description FROM activities WHERE userid = ?")
        cur.execute(sql, (userid,))
        activities = []
        for row in cur:
            (activity_id, title, date, location, description) = row
            activities.append({
                "activity_id": activity_id,
                "title": title,
                "date": date,
                "location": location,
                "description": description
            })
        return activities
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()


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
            #user does not exist
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
            #user does not exist
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


if __name__ == "__main__":
    try:
        conn = sqlite3.connect("database.db")
    except sqlite3.Error as err:
        print(err)
    else:
        #drop_table(conn)

        create_user_table(conn)
        create_activity_table(conn)
        create_participation_table(conn)

        add_user(conn, "johndoe", "John", "Doe", "johndoe@gmail.com", generate_password_hash("Joe123"), "admin")
        add_user(conn, "maryjane", "Mary", "Jane", "maryjane@gmail.com", generate_password_hash("LoveDogs"), "admin")
        
        add_new_activity(conn, "johndoe", "Joggetur rundt Mosvannet",  "2021-07-01", "Stavanger", "Dette er en aktivitet.")
        add_new_activity(conn, "maryjane", "Tur til Preikestolen",  "2021-07-01", "Stavanger", "Dette er en aktivitet2.")
        add_new_activity(conn, "johndoe", "Tur på Sola Strand",  "2021-07-01", "Stavanger", "Dette er en aktivitet2.")

        add_new_pacticipation(conn, 1, 1)

        print("USER",get_user_by_id(conn, 1))

        print("USER",get_user_by_name(conn, "johndoe"))
        
        hash = get_hash_for_login(conn, "maryjane")
        print("Check password: {}".format(check_password_hash(hash,"LoveDogs")))

        delete_activity(conn, 1)

        print(get_all_activities(conn))
        
        conn.close()
