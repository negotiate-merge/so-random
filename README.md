# So Random - README.md

This is my final project submission for CS50, titled So Random. At the onset of Covid I heard in the media of an $80 million powerball draw. I had recently been made redundant at work and thought I might try my luck with the lottery having not played lotto previously.

I navigated to a ticket vendor website and noticed they made reference to the frequency of ball numbers being drawn and that they had specified these numbers in to two catagory's, hot and cold. The website did not offer the functionality however to generate number sequences based on whether numbers were hot or cold.

Frustrated by this, I set out to create this functionality with my project.

## How does it work?

So Random is a web application that utilizes [Beautiful Soup](https://pypi.org/project/beautifulsoup4/) to scrape previous powerball draw results from the [Australia National-Lottery](https://australia.national-lottery.com/powerball/results-archive-2021) archive. The results are then archived in a mysql3 database running on the server.

The ball frequency statistics are taken from the past 52 weeks of results from the present date. The objective of the algorithm is to cast each ball into either the hot or cold catagory so that roughly half of each pool of balls lands in each catagory.

There are two pools of balls, game balls (there are 7 game balls drawn per draw) & power balls (there is 1 powerball drawn per draw).


## Description of files

### `app.py` 
This is the backbone of the application - it defines the functionality of the Flask web-server on which the web application is built. I have tried to keep this file as compact as possible to make it easier to read. There are three routes within the application:

`/` Ensures that the backend data to be served is current and serves and renders the homepage.

`/generate` Gets form data from the homepage and parses it to generate the random number sequences. The homepage allows the user to add additional parameter rows to the form throught the use of Javascript. The /generate route has the functionality to iterate over these added rows dynamically.

`/usage` Serves a page that shows the user how to use dev Tools to run the script in order to automate the process of filling the lottery vendors webform.

### `gen.py`
This file is where I have written all of my functions in order to keep them out of sight of the main application. Running through the functions from top to bottom:

`get_date(lastDrawn)` This function is called from the `dbUpdate` function. The purpose of this function is to detirmine if the last scraped draw added to the local database was in excess of 7 days prior to the current date. 

`aggregate(db)` pulls the last 52 weeks draws from the local database and detirmines each numbers catagory, hot or cold, for game balls and power balls.

`dbUpdate(URL, db)` is the function that does the web-scraping of the results. It will only run if the current date is greater than the next scheduled draw date via the use of `get_date`. It filters out the ad's that are present in the table of results, and reformates the data prior to inserting into the local database.

`drawBall(code)` returns a randomly generated game ball number dependent on the code that is passed in 'h for hot', 'c for cold' or 'r for random'

`drawPower(code)` the same as drawBall except returns a powerball

`changeState()` changes all of the aggregated numbers from the `aggregate` function from string types to int types. 

`getTemp(db)` originally this calculated last draw statistics for numerical presentation on the homepage. Most of it is deprecated now in favour of graphical representation using css. Now it just returns the the results of the last known draw for display on the home page.



