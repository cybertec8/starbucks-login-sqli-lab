"""
SQL Injection Practice Lab — "Free Starbucks Coffee" Login (Python / Flask)
-----------------------------------------------------------------------------
Intentionally vulnerable application for authorized cybersecurity training.
Use only in an isolated lab/classroom environment.
"""

import os
import sqlite3

from flask import Flask, render_template, request

app = Flask(__name__)


# ------------------------------------------------------------
# DATABASE SETUP
# ------------------------------------------------------------

db = sqlite3.connect(
    ":memory:",
    check_same_thread=False
)

db.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT
    )
""")

db.execute(
    "INSERT INTO users (username, password) VALUES (?, ?)",
    ("admin", "S3cretCoffeePw!")
)

db.commit()


# ------------------------------------------------------------
# LOGIN PAGE
# ------------------------------------------------------------

@app.route("/", methods=["GET"])
@app.route("/login", methods=["GET"])
def login_page():
    return render_template(
        "login.html",
        error=None
    )


# ------------------------------------------------------------
# LOGIN SUBMISSION
# ------------------------------------------------------------

@app.route("/login", methods=["POST"])
def login_submit():

    username = request.form.get("username", "")
    password = request.form.get("password", "")

    # Intentionally vulnerable SQL query for the authorized lab.
    query = (
        f"SELECT * FROM users "
        f"WHERE username = '{username}' "
        f"AND password = '{password}'"
    )

    print("Running query:", query)

    try:
        cursor = db.execute(query)
        rows = cursor.fetchall()

    except sqlite3.OperationalError as e:

        return render_template(
            "login.html",
            error=f"Query error: {e}"
        )

    if rows:
        return render_template("admin.html")

    return render_template(
        "login.html",
        error="Invalid username or password."
    )


# ------------------------------------------------------------
# START APPLICATION
# ------------------------------------------------------------

if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 5000)
    )

    print(
        f"Coffee login lab running on port {port}"
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
