import sqlite3
from flask import Flask, render_template, request
app = Flask(__name__)
@app.route('/')
@app.route('/index.jinja2')
def index():
    # connect to the database
    conn = sqlite3.connect("site_data.db")
    # Querying the database with SELECT statement
    cursor = conn.execute("SELECT User, Content, Likes, rowid from messages ORDER BY Likes DESC")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("index.jinja2", messages=records)

@app.route('/bike.jinja2')
def bike():
    return render_template("bike.jinja2")

@app.route('/about_me.jinja2')
def about_me():
    return render_template("about_me.jinja2")

@app.route('/locations.jinja2')
def locations():
    return render_template("locations.jinja2")

@app.route('/new_messages.jinja2', methods = ['POST'])
def custom():
    author = request.form['author']
    message = request.form['messages']
    # Connect to the database
    conn = sqlite3.connect("site_data.db")
    # Adding new data with the insert statement
    cursor = conn.execute("INSERT INTO messages VALUES (?, ?, 0)" % (author, message))
    cursor.close()
    conn.commit()
    conn.close()
    print("[%s] posted '%s' " % (author, message))

    return render_template("thanks.jinja2")

@app.route('/like.jinja2')
def like():
    rowid = request.args['rowid']
    # connect to the database
    conn = sqlite3.connect("site_data.db")
    # Querying the database with SELECT statement
    cursor = conn.execute("SELECT Likes from messages WHERE rowid=?", (rowid, ))
    record = cursor.fetchone()
    likes = record[0]
    cursor.close()
    # UPDATE the database with new like value
    cursor = conn.execute("UPDATE messages SET Likes=? WHERE rowid=?", (likes+1, rowid))
    conn.commit()
    cursor.close()
    conn.close()
    return render_template("thanks.jinja2")