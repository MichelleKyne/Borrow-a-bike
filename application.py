import pymysql
from jinja2 import Template
from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def index():
    
    try:
        f = open('weatherkey.txt')
        line = f.readlines() 
        converted_list=[]
    
        for element in line:
            converted_list.append(element.strip())
    
    #initalising variables
        host=converted_list[1]
        db_name=converted_list[2]
        user_name=converted_list[3]
        password=converted_list[4]
        
        connectionObject = pymysql.connect(host = host,user = user_name,passwd = password,db = db_name,port=3306)
        cursorObject = connectionObject.cursor()
        sqlQuery= "SELECT *  FROM dubBikes.Weather WHERE id = (SELECT MAX(id) FROM dubBikes.Weather)" 
        cursorObject.execute(sqlQuery)
        posts = cursorObject.fetchall()
        for row in posts:
            cloud = row[1]
            condition_icon=row[2]
            condition_text=row[3]
            precip_mm=row[7]
            temp_c=row[8]
            wind_kph=row[9]
                            
                    
                # Now print fetched result
            print ("cloud = %s ,condition_icon = %s,condition_text = %s ,precip_mm=%s,temp_c = %s,wind_kph=%s" % \
                   (cloud,condition_icon,condition_text,precip_mm,temp_c,wind_kph))
            
        return render_template("index.html",posts=posts)

    except:
        print("can't access database")
    
        return render_template("index.html")
    
if __name__ == "__main__":
    app.run(debug=True)
