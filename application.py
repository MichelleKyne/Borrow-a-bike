import pymysql
from jinja2 import Template
from flask import Flask, jsonify, render_template
import json
from email.policy import default

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/stations")
def stations():
    f = open('dynamickey.txt')
    line = f.readlines()
    converted_list = []

    for element in line:
        converted_list.append(element.strip())

    # initalising variables
    host = converted_list[0]
    db_name = converted_list[1]
    user_name = converted_list[2]
    password = converted_list[3]
        
    db = pymysql.connect(host=host, user=user_name, passwd=password, db=db_name, port=3306)
    cursor = db.cursor()
    cursor.execute("SELECT num,name,address,latitude,longitude,bike_stands,stands_free,bikes_free, MAX(last_update) AS most_recent FROM dublinbikes.dbikes GROUP BY num;")
    row_headers = [x[0] for x in cursor.description]
    data = cursor.fetchall()
    # create an array to store the sql data
    json_data = []
    for result in data:
        json_data.append(dict(zip(row_headers, result)))
    # convert the array to json format (default=str ensures dates are serializable) and return it
    return json.dumps(json_data,default=str)

@app.route("/stations/map")
def map():
    return render_template("map.html")
    
@app.route("/weather")
def weather():
    try:
        f = open('weatherkey.txt')
        line = f.readlines()
        converted_list = []

        for element in line:
            converted_list.append(element.strip())

        # initalising variables
        host = converted_list[1]
        db_name = converted_list[2]
        user_name = converted_list[3]
        password = converted_list[4]

        connectionObject = pymysql.connect(host=host, user=user_name, passwd=password, db=db_name, port=3306)
        cursorObject = connectionObject.cursor()
        sqlQuery = "SELECT *  FROM dubBikes.Weather WHERE id = (SELECT MAX(id) FROM dubBikes.Weather)"
        cursorObject.execute(sqlQuery)
        posts = cursorObject.fetchall()
        for row in posts:
            cloud = row[1]
            condition_icon = row[2]
            condition_text = row[3]
            precip_mm = row[7]
            temp_c = row[8]
            wind_kph = row[9]

            # Now print fetched result
            print("cloud = %s ,condition_icon = %s,condition_text = %s ,precip_mm=%s,temp_c = %s,wind_kph=%s" % \
                  (cloud, condition_icon, condition_text, precip_mm, temp_c, wind_kph))

        return render_template("weather.html", posts=posts)

    except:
        print("can't access database")

        return render_template("weather.html")

if __name__ == "__main__":
    app.run(debug=True)
