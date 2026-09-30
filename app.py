"""
SQL Injection Practice Lab — "Free Starbucks Coffee" Login (Python / Flask)
-----------------------------------------------------------------------------
⚠️ THIS APP IS INTENTIONALLY VULNERABLE. Built for students to practice
SQL injection against, on their own machine, for learning purposes only.
NEVER deploy code like this to a real/public server.

The vulnerability: the login query is built with an f-string that pastes
user input directly into the SQL, instead of using parameterized queries
(the "?" placeholder style). This lets an attacker inject SQL syntax
through the username/password fields and change the query's logic
(classic "auth bypass" SQLi).
"""

from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# --- Set up an in-memory database with one legit user ---
db = sqlite3.connect(":memory:", check_same_thread=False)
db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
db.execute(
    "INSERT INTO users (username, password) VALUES (?, ?)",
    ("admin", "S3cretCoffeePw!"),  # student does NOT know this password
)
db.commit()


@app.route("/", methods=["GET"])
@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html", error=None)


@app.route("/login", methods=["POST"])
def login_submit():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    # VULNERABLE: raw string interpolation into SQL. Try entering
    #   username:  ' OR '1'='1' --
    #   password:  anything
    # This makes the WHERE clause always true, logging in without the
    # real password.
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print("Running query:", query)  # shown in the terminal so students can see the injected SQL

    try:
        cursor = db.execute(query)
        rows = cursor.fetchall()
    except sqlite3.OperationalError as e:
        # A syntax error is itself a helpful clue during injection practice
        return render_template("login.html", error=f"Query error: {e}")

    if rows:
        return render_template("admin.html")
    else:
        return render_template("login.html", error="Invalid username or password.")


if __name__ == "__main__":
    print("Coffee login lab running: http://localhost:5000")
    app.run(debug=True, port=5000)
