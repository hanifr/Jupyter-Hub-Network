import os
import hashlib
from flask import Flask, redirect, url_for, request, render_template
from flask import abort, session, jsonify, flash, g
import sqlite3
import mysql.connector as mariadb


app = Flask(__name__)
app.secret_key = b'_5#y2L"412124las1gn7((9as18z\n\xec]/'

DATABASE = "data/user.db"
MARIADB_USER = "root"
# The environment variable ROOT_PASSWORD_FILE will be set via docker-compose.
# ADMIN_PASSWORD = open(os.environ['ROOT_PASSWORD_FILE'], 'r').read()
ADMIN_PASSWORD = "geheim"

INITIAL_SCHEMA = ("CREATE Table Users("
                  "Username TEXT PRIMARY KEY,"
                  "Activated INTEGER NOT NULL,"
                  "Password TEXT NOT NULL);")

INITIAL_INSERT = ("INSERT INTO Users VALUES "
                  "('hubadmin', 1, ?);")

CREATE_USER = ("CREATE USER %s "
               "IDENTIFIED BY %s;")
GRANT_ACCESS = ("GRANT SELECT "
                "ON *.* "
                "TO %s@'%';")


def hashfunc(password):
    """Hashes a given password using SHA512.

    Arguments:
        password {string} -- The password to hash.

    Returns:
        string -- Hexadecimal digest of the hashed password.
    """
    return hashlib.sha512(password.encode('utf-8')).hexdigest()


def get_db():
    """Returns the database connection object.
    If no database exists (typically the case on the first call),
    it will be created and atttached to the `flask.g` object.

    Returns:
        sqlite3.Connection -- The sqlite3 connection object.
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def user_exists(username):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT Username FROM Users WHERE Username=?", (username,))
    result = c.fetchone()
    if result is not None:
        return result[0]
    else:
        return None


def get_activated_and_password(username):
    """Retrieves the Activated-status and password for a
    given username from the database

    Arguments:
        username {string} -- Username

    Returns:
        (int, string) or None -- Tuple of Activated-status (1 for activated,
        0 otherwise) and the hashed password for the username. `None` if the
        user does not exists.
    """
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT Activated, Password FROM Users WHERE Username=?", (username,))
    r = c.fetchone()
    return r


def insert(username, activated, hashed_pw):
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO Users VALUES (?,?,?)", (username, 1, hashed_pw))
    conn.commit()


@app.before_first_request
def create_database_if_not_exists():
    if not os.path.isfile(DATABASE):
        conn = get_db()
        c = conn.cursor()
        # Create the database schema and insert the 'hubadmin'.
        c.execute(INITIAL_SCHEMA)
        hased_pw = hashfunc(ADMIN_PASSWORD)
        c.execute(INITIAL_INSERT, (hased_pw, ))
        conn.commit()
        print("Created initial database.")


@app.route('/')
def index():
    if 'username' in session:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        users = c.execute('SELECT * FROM Users').fetchall()
        conn.close()
        return render_template('all.html', users=users)
    else:
        return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.form['username']
        password = request.form['password']
    except KeyError:
        return "Error"
    else:
        if username != 'hubadmin':
            error = 'Either password or username wrong.'
            return render_template('login.html', error=error)
        _, hash_from_db = get_activated_and_password('hubadmin')
        if hashfunc(password) == hash_from_db:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            error = 'Either password or username wrong.'
            return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/adduser', methods=['POST'])
def adduser():
    try:
        username = request.form['username']
        password = request.form['password']
        repeated_password = request.form['repeated_password']
    except KeyError:
        return "Error"
    else:
        if password != repeated_password:
            flash('Password do not match.')
            return redirect(url_for('index'))
        # Check if username if available.
        if user_exists(username) is not None:
            flash('User already exists.')
            return redirect(url_for('index'))
        # Add user to user database.
        hashed_pw = hashfunc(password)
        insert(username, 1, hashed_pw)
        # Add user to maria database.
        # TODO Error handling.
        mariadb_connection = mariadb.connect(
            host='database',
            user=MARIADB_USER,
            password=ADMIN_PASSWORD,
            database='mysql')
        cur = mariadb_connection.cursor()
        cur.execute(CREATE_USER, (username, password))
        cur.execute(GRANT_ACCESS, (username, ))
        mariadb_connection.close()
        # cursor = mariadb_connection.cursor()
        flash('Added user {}.'.format(username))
        return redirect(url_for('index'))


@app.route('/auth', methods=['POST'])
def authentificate():
    try:
        username = request.json["username"]
        password = request.json["password"]
    except KeyError:
        abort(405)
    else:
        a, p = get_activated_and_password(username)
        if a is not None and a == 1 and p == hashfunc(password):
            return jsonify(access=True)
        else:
            return jsonify(access=False)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
