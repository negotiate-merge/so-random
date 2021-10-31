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

`/` Ensures that the backend data to be served is current and serves and renders the homepage

`/generate` Gets form data from the homepage and parses it to generate the random number sequences. The homepage allows the user to add additional parameter rows to the form throught the use of Javascript. The /generate route has the functionality to iterate over these added rows dynamically.

`/usage` Serves a page that shows the user how to use dev Tools to run the script in order to automate the process of filling the lottery vendors webform.




if you debated certain design choices, explaining why you made them. 

Ensure you allocate sufficient time and energy to writing a README.md that you are proud of and that documents your project thoroughly. Be proud of it!
