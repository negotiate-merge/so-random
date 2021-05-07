from cs50 import SQL
import csv
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from gen import *
import requests
import sys


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure DB
db = SQL("sqlite:///silo.db")

# URL for web scraping results
URL = 'https://australia.national-lottery.com/powerball/results-archive-2021'

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/', methods=["GET", "POST"])
def index():
    """ Show recent draw stats and provide interface for user input to generate numbers """
    if request.method == "GET":
        # Ensure database has the latest draw results
        dbUpdate(URL, db)

        # Aggregate ball counts
        aggregated = aggregate(db)

        # Get temp stats of last draw
        stat = getTemp(db)
       
        # Retrieve additional info for display on home page
        lastRecord = db.execute("SELECT MAX(drawDate) AS drawDate FROM results")[0]['drawDate']
        latestDate = f"{lastRecord[8:]}-{lastRecord[5:7]}-{lastRecord[0:4]}"

        return render_template('index.html', latest=latestDate, coldNumbers=", ".join(aggregated['coldNumbers']), 
        hotNumbers=", ".join(aggregated['hotNumbers']), coldPowers=", ".join(aggregated['coldPowers']), 
        hotPowers=", ".join(aggregated['hotPowers']), hotNums=stat['hot'], coldNums=stat['cold'], power=stat['power'],
        ldn=", ".join(stat['lastNums']), ldp=stat['lastPower'])
        

@app.route("/generate", methods=["GET", "POST"])
def generate():
    if request.method == "POST":
        # Get paramters from web form
        hh = int(request.form.get('hh'))
        hc = int(request.form.get('hc'))
        ch = int(request.form.get('ch'))
        cc = int(request.form.get('cc'))
        r = int(request.form.get('r'))
        h = int(request.form.get('h'))
        custom = int(request.form.get('c'))
        power = request.form.get('power')

        # Store the generated numbers
        thisDraw = []

        changeState()
        # Hot Hot generator
        print("hh")
        while hh > 0:
            balls = 0
            drawn = []
            while balls < 7:
                b = drawBall('h')
                if b not in drawn:
                    drawn.append(b)
                    balls += 1
            drawn.append(drawPower('h'))
            thisDraw.append(drawn)
            hh -= 1

        # Hot Cold generator
        print("hc")
        while hc > 0:
            balls = 0
            drawn = []
            while balls < 7:
                b = drawBall('h')
                if b not in drawn:
                    drawn.append(b)
                    balls += 1
            drawn.append(drawPower('c'))
            thisDraw.append(drawn)
            hc -= 1

        # Cold Cold generator
        print("cc")
        while cc > 0:
            balls = 0
            drawn = []
            while balls < 7:
                b = drawBall('c')
                if b not in drawn:
                    drawn.append(b)
                    balls += 1
            drawn.append(drawPower('c'))
            thisDraw.append(drawn)
            cc -= 1

        # Cold Hot generator
        print("ch")
        while ch > 0:
            balls = 0
            drawn = []
            while balls < 7:
                b = drawBall('c')
                if b not in drawn:
                    drawn.append(b)
                    balls += 1
            drawn.append(drawPower('h'))
            thisDraw.append(drawn)
            ch -= 1

        # Random generator
        print("r")
        while r > 0:
            balls = 0
            drawn = []
            while balls < 7:
                b = drawBall('r')
                if b not in drawn:
                    drawn.append(b)
                    balls += 1
            drawn.append(drawPower('r'))
            thisDraw.append(drawn)
            r -= 1

        # Custom generator
        while custom > 0:
            balls = 0
            drawn = []
            while balls < h:
                b = drawBall('h')
                if b not in drawn:
                    drawn.append(b)
                    balls += 1
            while balls < 7:
                b = drawBall('c')
                if b not in drawn:
                    drawn.append(b)
                    balls += 1
            if power == 'hot':
                drawn.append(drawPower('h'))
            else:
                drawn.append(drawPower('c'))
            thisDraw.append(drawn)
            custom -= 1

        print(thisDraw)
        # Open the buy tickets page in a new tab and insert numbers into the form

        
        
        return render_template("/numbers.html", message="Your lotto numbers", link="Return to Parameter Selection", lines=thisDraw)
    else:
        return render_template("/error.html", message="No numbers here", link="Return home to Enter Parameters.")
