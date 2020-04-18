import sqlite3
from flask import Flask, render_template, request
import requests
app = Flask(__name__)

OPEN_WEATHER_KEY = "e002e4a56551adbd797f982bf7bca49f"
IP_STACK_KEY = "5918148b7bf91a2041923d9602e680e6"


@app.route('/')
@app.route('/index.jinja2')
def index():
    # connect to the database
    conn = sqlite3.connect("site_data.db")
    # Querying the database with SELECT statement
    cursor = conn.execute("SELECT User, Content, Likes, rowid from messages ORDER BY Likes DESC")
    records = cursor.fetchall()
    cursor = conn.execute("SELECT DISTINCT location FROM messages")
    locations = cursor.fetchall()
    loc_data = get_location_data(request.remote_addr)
    lat = loc_data['latitude']
    long = loc_data['longitude']
    (temperature,weather_description) = get_weather_data(lat, long)

    # get the client's IP address
    ip_addr = request.remote_addr
    loc_data = get_location_data(ip_addr)
    if temperature > 50:
        temperature_style = 'text-danger'
    else:
        temperature_style = 'text-primary'
    cursor.close()
    conn.close()
    return render_template("index.jinja2", messages=records, weather_description=weather_description,
                                                        temperature_style=temperature_style,
                                                            temperature = "%0.2f"%temperature,
                                                            msg_locations = locations)

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
    # add some location information to the author
    loc_data = get_location_data(request.remote_addr)
    author = author + " from %s, %s" % (loc_data['city'], loc_data['region_code'])
    message = request.form['messages']
    # Connect to the database
    conn = sqlite3.connect("site_data.db")
    # Adding new data with the insert statement
    location = "%s/%s" % (loc_data['country_code'], loc_data['region_code'])
    location = location.lower()
    cursor = conn.execute("INSERT INTO messages VALUES (?, ?, 0, ?)" , (author, message, location))
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

def get_weather_data(lat, long):
    lat = 38.981119
    long = -76.486269
    resp = requests.get("http://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&appid=%s" % (lat, long,
                                                                                                   OPEN_WEATHER_KEY))
    result = resp.json()
    desc = result['weather'][0]['description']
    temp = (result['main']['temp'] - 273.15)*9/5+32
    return temp,desc

def get_location_data(ip_addr):
    resp = requests.get("http://api.ipstack.com/%s?access_key=%s" % (ip_addr, IP_STACK_KEY))
    result = resp.json()
    if result['latitude'] is None:
        result['city'] = 'Annapolis'
        result['latitude'] = 38.981119
        result['longitude'] = -76.486269
        result['country_code'] = 'US'
        result['region_code'] = 'MD'
        result['region_name'] = 'Maryland'
    return result











