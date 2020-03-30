from flask import Flask, render_template
app = Flask(__name__)

@app.route('/index.html')
def index():
    return render_template("index.jinja2")

@app.route('/bike.html')
def bike():
    return render_template("bike.jinja2")

@app.route('/about_me.html')
def about_me():
    return render_template("about_me.jinja2")

@app.route('/locations.html')
def locations():
    return render_template("locations.jinja2html")