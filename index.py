#!C:/Python27/Python
import MySQLdb
import sys
import os
from flask import Flask,redirect,url_for,render_template,request,session
from werkzeug import secure_filename

app = Flask(__name__)

app.secret_key = os.urandom(24)

@app.route("/", methods = ["GET", "POST"])
def Login_Page():

    return render_template("login.html")

@app.route("/dashboard", methods = ["GET","POST"])
def dashboard_page():
    
    hostname = "localhost"
    username = "root"
    password = ""
    database = "datacenter"

    connection = MySQLdb.connect(hostname, username, password, database)
    cur = connection.cursor()

    if request.method == "POST":
        session["mail"] = request.form["admin_email"]
        session["pass"] = request.form["admin_password"]

        if request.form["admin_email"] == None or request.form["admin_password"] == None or request.form["admin_email"] != "admin" or request.form["admin_password"] != "admin":
            return redirect(url_for("Login_Page"))

    if "mail" in session or "pass" in session:
        
        sql_query = "SELECT * FROM users WHERE user_id > 0 ORDER BY user_id DESC"
        cur.execute(sql_query)
        user_data = cur.fetchall()

        return render_template("index.html", usdata = user_data)
    else:
        return redirect(url_for("Login_Page"))

@app.route("/logout")
def logout():
    session.clear()

    return redirect(url_for("Login_Page"))
            

if __name__ == "__main__":
    app.run(debug = True)