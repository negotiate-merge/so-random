# So Random - README.md

## Video demo: <https://youtu.be/ye47GN2qDiQ>

This is my final project submission for CS50, titled So Random. At the onset of Covid I heard in the media of an $80 million Powerball draw. I had recently been made redundant at work and thought I might try my luck with the lottery having not played lotto previously.

I navigated to a ticket vendor website and noticed they made reference to the frequency of ball numbers being drawn and that they had specified these numbers in to two category's, hot and cold. The website did not offer the functionality however to generate random number sequences based on hot or cold numbers.

Frustrated by this, I set out to create this functionality with my project.

## How does it work?

So Random is a web application that utilizes [Beautiful Soup](https://pypi.org/project/beautifulsoup4/) to scrape previous Powerball draw results from the [Australia National-Lottery](https://australia.national-lottery.com/powerball/results-archive-2021) archive. The results are then archived in a mysql3 database running on the server.

The ball frequency statistics are taken from the past 52 weeks of results from the present date. The objective of the algorithm is to cast each ball into either the hot or cold category so that roughly half of each pool of balls lands in each category.

There are two pools of balls, game balls (7 game balls per draw) & power balls (1 Powerball per draw).

The application allows the user to configure their ball draw preferences from the homepage. Hitting the get numbers button will generate random number sequences as specified and  present them on a new page.

Hitting the "Use these Numbers" button will copy a pre-formatted JavaScript function to the clipboard and redirect the user to a page that has instructions for use for the automated insertion of these numbers into a [lotto vendors](https://www.ozlotteries.com/powerball) webform.


## Description of files

### `app.py` 
This is the backbone of the application - it defines the functionality of the Flask web-server on which the web application is built. I have tried to keep this file as compact as possible to make it easier to navigate. There are three routes within the application:

`/` Ensures that the backend data to be served is current and serves the homepage.

`/generate` Gets form data from the homepage and parses it to generate the random number sequences. The homepage allows the user to add additional parameter rows to the form through the use of JavaScript. The /generate route has the functionality to iterate over these added rows dynamically.

`/usage` Serves a page that shows the user how to use dev tools to run the script in order to automate the process of filling the lottery vendors webform.

### `gen.py`
This file is where I have written all of my functions in order to keep them out of sight of the main application. Running through the functions from top to bottom:

`get_date(lastDrawn)` This function is called from the `dbUpdate` function. The purpose of this function is to determine if the last scraped draw added to the local database was in excess of 7 days prior to the current date. 

`aggregate(db)` pulls the last 52 weeks draws from the local database and determines each numbers category, hot or cold, for game balls and power balls.

`dbUpdate(URL, db)` is the function that does the web-scraping of the results. It will only run if the current date is greater than the next scheduled draw date via the use of `get_date`. It filters out the ad's that are present in the table of results, and inserts the missing drawn numbers into the local database.

`drawBall(code)` returns a randomly generated game ball number dependent on the code that is passed in 'h' for hot, 'c' for cold or 'r' for random.

`drawPower(code)` the same as drawBall except returns a Powerball

`changeState()` changes all of the aggregated numbers from the `aggregate` function from string types to int types. 

`getTemp(db)` originally this calculated statistics for the last draw for display on the homepage. Most of it is deprecated now in favor of graphical representation using CSS. Now it just returns the results of the last known draw for display on the home page.


### `syntech.js`
This is the where the bulk of the JavaScript that I have written for this project resides. There is some JavaScript code embedded within the applications html files which is fairly well commented and mainly interacts with this file.

At the top of the file I have some ball objects that are used to categorize each pool of balls into their respective heat class.

`returnNumbers(element)` Elements are passed in to this function by id from index.html - the element arguments are already sorted into heat categories from the back end which is determinable by the id of the element. The function then populates the ball objects mentioned above. This is in place to allow dynamic CSS styling, so that the user can see which balls are hot or cold in any given sequence.

`populateStorage()` This function sets sessionStorage with the values that are contained within the ball objects. This allows these values to be accessed across pages which is essential for styling of the generated balls numbers.

`color(num, category)` Dependent on the number and ball type passed in as arguments. Returns True if cold otherwise returns False.

`addRow()` This function allows for the creation of additional rows in the parameter selection table on the home page.

`copyScript()` copies the code snippet including the generated numbers to the clipboard.

### silo.db
This is the local database of archived lottery results.

## Design Choices
I wanted to create a web application that was sufficiently complex it its design without being to cumbersome for the user. CS50 teaches us to create user accounts and to utilize a login page. I have left these components out of this project in favor of ease of use, generating random numbers in this case does not require any security.


