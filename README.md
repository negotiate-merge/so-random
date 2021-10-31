# So Random - README.md

should explain what your project is
This is my final project submission for CS50, titled So Random. At the onset of Covid I heard in the media of an $80 million powerball draw. I had recently been made redundant at work and thought I might try my luck with the lottery having not played lotto previously. I navigated to a ticket vendor website and noticed they made reference to the frequency of ball numbers being drawn and that they had specified these numbers in to two catagory's, hot and cold. The website did not offer the functionality however to generate number sequences based on whether numbers were hot or cold. Frustrated by this, I set out to create this functionality with my project.

## How does it work?

So Random is a web application that utilizes [Beautiful Soup](https://pypi.org/project/beautifulsoup4/) to scrape previous powerball draw results from the [Australia National-Lottery](https://australia.national-lottery.com/powerball/results-archive-2021) archive. The results are then archived in a mysql3 database running on the server. 
The ball frequency statistics are taken from the past 52 weeks of results from the present date. The objective of the algorithm is to cast each ball into either the hot or cold catagory so that roughly half of each pool of balls lands in each catagory. 
There are two pools of balls, game balls (there are 7 game balls drawn per draw) & power balls (there is 1 powerball drawn per draw).


## Description of files

`app.py` is the backbone of the application - it defines the Flask web-server and handles all of the backend functionality. I have tried to keep this file compact to make it easier to deal with 

multiple paragraphs in length

what each of the files you wrote for the project contains and does
if you debated certain design choices, explaining why you made them. 

Ensure you allocate sufficient time and energy to writing a README.md that you are proud of and that documents your project thoroughly. Be proud of it!
