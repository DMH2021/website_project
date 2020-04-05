from flask import Flask, render_template, request
app = Flask(__name__)
@app.route('/')
@app.route('/index.jinja2')
def index():
    return render_template("index.jinja2")

@app.route('/bike.jinja2')
def bike():
    return render_template("bike.jinja2")

@app.route('/about_me.jinja2')
def about_me():
    return render_template("about_me.jinja2")

@app.route('/locations.jinja2')
def locations():
    return render_template("locations.jinja2")

@app.route('/custom.jinja2', methods = ['POST'])
def custom():
    fname = request.form['fname']
    lname = request.form['lname']
    name = fname + " " + lname

    thing = request.form['favorite_thing']
    if thing == "BMC":
        image_paths = 'static/BMC.jpg'
    elif thing == "Cervelo":
        image_paths = 'static/Cervelo.jpg'
    elif thing == "Trek":
        image_paths = 'static/Trek.jpg'
    elif thing == "Canyon":
        image_paths = 'static/Canyon.jpg'
    elif thing == "Pinarello":
        image_paths = 'static/Pinarello.jpg'
    return render_template("custom.jinja2", full_name = name, image_paths = image_paths)