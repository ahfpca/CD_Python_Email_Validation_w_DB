from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import MySQLConnection
import re, datetime

app = Flask(__name__)
app.secret_key = "sdjvnwpeiugh3498fh"


mysql = MySQLConnection('emailValidDB')
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


@app.route("/", methods=["get"])
def index():
    # Fetch records from table
    data = mysql.query_db("SELECT * FROM emails")

    return render_template("index.html", data = data)


@app.route("/register", methods=["post"])
def register():
    # Validate data
    email = request.form["email"]
    if len(email) < 1:
        flash("Email can not be empty!", "error")
        session["email"] = email
    elif not email_regex.match(email):
        flash("Email is not valid!", "error")
        session["email"] = email
    else: 
        # Save it to table
        sqlCmd = "INSERT INTO emails (email, created_at) VALUES (%(email)s, %(created_at)s)"
        
        fields = {  'email': email,
                    'created_at': datetime.datetime.now() }

        ret = mysql.query_db(sqlCmd, fields)
        if ret > 0:
            flash(f"Email [{ email }] registered successfully!", "message")
            session["email"] = ""
        else:
            flash("Something went wrong!", "error")
            session["email"] = email
            
    return redirect("/")


@app.route("/delete/<id>")
def delete(id):
    # Delete id from table
    data = { 'id': id }

    mysql.query_db("DELETE FROM emails WHERE id = %(id)s", data)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug = True)
