import pymysql
from jinja2 import Template
from flask import Flask, render_template
import json

app = Flask(__name__)


@app.route("/")
def index():
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

        return render_template("index.html", posts=posts)

    except:
        print("can't access database")

        return render_template("index.html")


@app.route("/stations")
def stations():
    # engine = create_engine("mysql+mysqlconnector://{}:{}@{}:{}/{}".format("Praneeth", "Praneeth@043", "dbbikes.cporu4f1xwew.us-east-1.rds.amazonaws.com", 3306, "dbikes"), echo=True)
    link = "dbbikes.cporu4f1xwew.us-east-1.rds.amazonaws.com"
    db = pymysql.connect(host="dbbikes.cporu4f1xwew.us-east-1.rds.amazonaws.com", port=int(3306), user="Praneeth",
                         passwd="Praneeth043")
    cursor = db.cursor()

    # get all the columns in the station table and the available bikes, bike stands details from availability table
    cursor.execute(
        "select S.*,A.available_bikes, A.available_bike_stands from dbikes.station S join dbikes.availability A on S.id = A.id")

    row_headers = [x[0] for x in cursor.description]
    data = cursor.fetchall()
    print([i for i in data])

    # create an array to store the sql sata
    json_data = []
    for result in data:
        json_data.append(dict(zip(row_headers, result)))

    # convert the array to json format and return it
    return json.dumps(json_data)


if __name__ == "__main__":
    app.run(debug=True)
