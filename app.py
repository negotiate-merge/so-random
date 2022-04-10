from cs50 import SQL
from flask import Flask, render_template, request
from flask_session import Session
from tempfile import mkdtemp
from gen import *


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure DB
db = SQL("sqlite:///silo.db")

# URL for web scraping results
URL = 'https://australia.national-lottery.com/powerball/results-archive-2022'

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
        aggregated = aggregate(db, 52)
        # Ball heat for accurate display of the previous draw heat
        lastAggregated = aggregate(db, 53)

        # Get temp stats of last draw
        stat = getTemp(db)
       
        # Retrieve additional info for display on home page
        lastRecord = db.execute("SELECT MAX(drawDate) AS drawDate FROM results")[0]['drawDate']
        # Reformat date 
        latestDate = f"{lastRecord[8:]}-{lastRecord[5:7]}-{lastRecord[0:4]}"

        return render_template('index.html', latest=latestDate, previousColdNums=lastAggregated['coldNumbers'], 
        previousHotNums=lastAggregated['hotNumbers'], previousColdPows=lastAggregated['coldPowers'],
        previousHotPows=lastAggregated['hotPowers'], coldNumbers=aggregated['coldNumbers'], 
        hotNumbers=aggregated['hotNumbers'], coldPowers=aggregated['coldPowers'], 
        hotPowers=aggregated['hotPowers'], ldn=stat['lastNums'], ldp=stat['lastPower'])


@app.route("/generate", methods=["GET", "POST"])
def generate():
    if request.method == "POST":
        # Store Drawn numbers
        thisDraw = []

        # Generate random numbers
        randomNos = int(request.form.get('random'))
        while randomNos > 0:
            balls = 0
            drawn = []
            while balls < 7:
                b = drawBall('r')
                if b not in drawn:
                    drawn.append(b)
                    balls += 1
            drawn.append(drawPower('r'))
            thisDraw.append(drawn)
            randomNos -= 1

        # Converts stringified numbers to integers
        changeState()

        '''
        Dynamic generation of hot cold selections
        '''
        # Integer for concatenation to names
        rowCount = 1

        while ('hot' + str(rowCount)) in request.form:
            names = ['hot', 'power', 'count']

            # Dynamic key name assignment for form
            hotRow = names[0] + str(rowCount)
            powerRow = names[1] + str(rowCount)
            countRow = names[2] + str(rowCount)

            # Get values from web form
            hot = int(request.form.get(f'{hotRow}'))
            count = int(request.form.get(f'{countRow}'))
            power = request.form.get(f'{powerRow}')
            
            # Variable heat number generator
            # For each line
            while count > 0:
                balls = 0
                drawn = []
                # Generate hot balls
                while balls < hot:
                    b = drawBall('h')
                    if b not in drawn:
                        drawn.append(b)
                        balls += 1
                # Generate cold balls
                while balls < 7:
                    b = drawBall('c')
                    if b not in drawn:
                        drawn.append(b)
                        balls += 1
                # Generate power ball
                if power == 'hot':
                    drawn.append(drawPower('h'))
                else:
                    drawn.append(drawPower('c'))
                thisDraw.append(drawn)
                count -= 1
            
            # Increment concatenation counter at top of main loop
            rowCount += 1

        return render_template("/numbers.html", message="Your lotto numbers", link="Return to Parameter Selection", lines=thisDraw)
    else:
        return render_template("/error.html", message="Woops, you seem to have lost your way", link="Return home to Enter Parameters.")

@app.route("/usage", methods=["GET"])
def usage():
    if request.method == 'GET':
        return render_template("/usage.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
