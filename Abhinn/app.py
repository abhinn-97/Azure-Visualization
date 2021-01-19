from flask import Flask, render_template, request
import time
import psycopg2
import redis
import _pickle as cPickle
import hashlib
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'blah blah blah blah'
myHostname = "abhiredis.redis.cache.windows.net"
myPassword = "Iu4V5SF1XD1QnJfizjj9NcJSMhJpf9Y3+lLtVxcTkn0="

pool = redis.ConnectionPool(host=myHostname, 
                            port=6380,
                            password=myPassword,
                            db=0, 
                            connection_class=redis.SSLConnection, 
                            ssl_cert_reqs=u'none')
                            
client = redis.Redis(connection_pool=pool)
conn = psycopg2.connect(
                host = "abhipost.postgres.database.azure.com",
                dbname = "abhiadb",
                user = "Abhi@abhipost",
                password = "Azureadb2020",
                sslmode = "require"
            )
cur = conn.cursor()

@app.route("/") 
def index():
    return render_template("index.html")

@app.route("/question7")
def question7():
    return render_template("terrorist.html")

@app.route("/question7", methods=['POST'])
def showquestion7():
    start = time.time()
    code = request.form['country']
    query = "SELECT SP.Code, SP.Entity, SP.Year, SP.Cost, TI.NumberTerroristIncidents FROM SP INNER JOIN TI ON SP.Code = TI.Code WHERE SP.Code = '" + code + "' AND SP.YEAR=TI.Year"
    cur.execute(query)
    row = cur.fetchall()
    end = time.time()
    totaltime = end - start
    return render_template("showterrorist.html", data=row, timetaken=totaltime)


@app.route("/question8")
def question8():
    return render_template("range.html")

@app.route("/question8", methods=['POST'])
def showquestion8():
    start = time.time()
    loweryear = request.form['loweryear']
    upperyear = request.form['upperyear']
    query = "SELECT SP.Code, SP.Entity, SP.Year, SP.Cost, TI.NumberTerroristIncidents FROM SP INNER JOIN TI ON SP.Code = TI.Code WHERE SP.YEAR >= '" + loweryear + "' AND SP.YEAR <= '" + upperyear + "'AND SP.YEAR=TI.Year"
    cur.execute(query)
    row = cur.fetchall()
    end = time.time()
    totaltime = end - start
    return render_template("showterrorist.html", data=row , timetaken=totaltime)


@app.route("/question9")
def question9():
    return render_template("sprange.html")

@app.route("/question9", methods=['POST'])
def showquestion9():
    start = time.time()
    lowerrange = request.form['lowerrange']
    upperrange = request.form['upperrange']
    query = "SELECT SP.Code, SP.Entity, SP.Year, SP.Cost, TI.NumberTerroristIncidents FROM SP INNER JOIN TI ON SP.Code = TI.Code WHERE SP.Cost >= '" + lowerrange + "' AND SP.Cost <= '" + upperrange + "'AND SP.YEAR=TI.Year"
    cur.execute(query)
    row = cur.fetchall()
    end = time.time()
    totaltime = end - start
    return render_template("showterrorist.html", data=row , timetaken=totaltime)


@app.route("/question10")
def question10():
    return render_template("8times.html")

@app.route("/question10", methods=['POST'])
def showquestion10():
    start = time.time()
    loweryear = request.form['loweryear']
    upperyear = request.form['upperyear']
    times = request.form['times']
    totaltimes = int(times)
    count = 0
    sql = "SELECT SP.Code, SP.Entity, SP.Year, SP.Cost, TI.NumberTerroristIncidents FROM SP INNER JOIN TI ON SP.Code = TI.Code WHERE SP.YEAR >= '" + loweryear + "' AND SP.YEAR <= '" + upperyear + "'AND SP.YEAR=TI.Year"
    hash = hashlib.sha224(sql.encode('utf-8')).hexdigest()
    key = "sql_cache:" + hash
    if (client.get(key)):
        while count < totaltimes:
            cur.execute(sql)
            count += 1
        row = cur.fetchall()
        end = time.time()
        totaltime = end - start
        return render_template("showterrorist.html", data=row, timetaken=totaltime)
    else:
        while count < totaltimes:
            cur.execute(sql)
            count += 1
        row = cur.fetchall()
        end = time.time()
        totaltime = end - start
        client.set(key, cPickle.dumps(row))
        client.expire(key, 10000000)
        return render_template("showterrorist.html", data=row, timetaken=totaltime)


@app.route("/question102")
def question102():
    return render_template("9times.html")

@app.route("/question102", methods=['POST'])
def showquestion102():
    start = time.time()
    lowerrange = request.form['lowerrange']
    upperrange = request.form['upperrange']
    times = request.form['times']
    totaltimes = int(times)
    count = 0
    sql = "SELECT SP.Code, SP.Entity, SP.Year, SP.Cost, TI.NumberTerroristIncidents FROM SP INNER JOIN TI ON SP.Code = TI.Code WHERE SP.Cost >= '" + lowerrange + "' AND SP.Cost <= '" + upperrange + "'AND SP.YEAR=TI.Year"
    hash = hashlib.sha224(sql.encode('utf-8')).hexdigest()
    key = "sql_cache:" + hash
    if (client.get(key)):
        while count < totaltimes:
            cur.execute(sql)
            count += 1
        row = cur.fetchall()
        end = time.time()
        totaltime = end - start
        return render_template("showterrorist.html", data=row, timetaken=totaltime)
    else:
        while count < totaltimes:
            cur.execute(sql)
            count += 1
        row = cur.fetchall()
        end = time.time()
        totaltime = end - start
        client.set(key, cPickle.dumps(row))
        client.expire(key, 1000000)
        return render_template("showterrorist.html", data=row, timetaken=totaltime)



@app.route("/question11")
def question11():
    return render_template("8timescache.html")

@app.route("/question11", methods=['POST'])
def showquestion11():
    start = time.time()
    loweryear = request.form['loweryear']
    upperyear = request.form['upperyear']
    times = request.form['times']
    totaltimes = int(times)
    count = 0
    sql = "SELECT SP.Code, SP.Entity, SP.Year, SP.Cost, TI.NumberTerroristIncidents FROM SP INNER JOIN TI ON SP.Code = TI.Code WHERE SP.YEAR >= '" + loweryear + "' AND SP.YEAR <= '" + upperyear + "'AND SP.YEAR=TI.Year"
    hash = hashlib.sha224(sql.encode('utf-8')).hexdigest()
    key = "sql_cache:" + hash
    if (client.get(key)):
        while count < totaltimes:
            row = (cPickle.loads(client.get(key)))
            count += 1
        end = time.time()
        totaltime = end - start
        return render_template("showterrorist.html", data=row, timetaken=totaltime)
    else:
        return render_template("expire.html")

@app.route("/question112")
def question112():
    return render_template("9timescache.html")

@app.route("/question112", methods=['POST'])
def showquestion112():
    start = time.time()
    lowerrange = request.form['lowerrange']
    upperrange = request.form['upperrange']
    times = request.form['times']
    totaltimes = int(times)
    count = 0
    sql = "SELECT SP.Code, SP.Entity, SP.Year, SP.Cost, TI.NumberTerroristIncidents FROM SP INNER JOIN TI ON SP.Code = TI.Code WHERE SP.Cost >= '" + lowerrange + "' AND SP.Cost <= '" + upperrange + "'AND SP.YEAR=TI.Year"
    hash = hashlib.sha224(sql.encode('utf-8')).hexdigest()
    key = "sql_cache:" + hash
    if (client.get(key)):
        while count < totaltimes:
            row = (cPickle.loads(client.get(key)))
            count += 1
        end = time.time()
        totaltime = end - start
        return render_template("showterrorist.html", data=row, timetaken=totaltime)
    else:
        return render_template("expire.html")

port = int(os.getenv('PORT', '3000'))
app.run(host='0.0.0.0', port=port)