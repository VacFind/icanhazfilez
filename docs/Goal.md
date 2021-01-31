# Project Goal

The goal of this repo is to automate the process of scraping spreadsheets and other file-based vaccination distribution data that states and counties make available pulicly. I imagine this would act similarly to apps like visualping.io that watch a page for changes, but it watches for a new data dump about covid vaccines and saves it.

The app should work something like this:
1. a new data source is added to the database
2. when the scraper next runs (likely via a cronjob) it will check to see if it has scraped that same data already and only scrape if theres new data. Some ways to determine this:
	- HTTP headers/modification date
	- manually entering a time the datasource is expected to be updated (i.e. if they post at regular intervals)
	- checking the filename
	- downloading the file and checking its hash
3. Once it has been determined that there is new data, download it as a file and add it to the database as a raw_data record. Also possibly help keep an organized folder tree for the downloaded data (by state and date or something like that)

This is pretty much the end of the responsibility of this web-scraping program, however, from here, the data will be available in the sqlite DB for processing and parsing into a more standard table structure, or something.

This DB may also eventually get merged with others to form a larger database backend for more general COVID vaccine data intake, processing, and display to users.

