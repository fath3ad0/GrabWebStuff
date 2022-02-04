# GrabWebStuff 
Quick and dirty script to grab links and forms from target site

### Purpose/Usage 
This was a quick and dirty script to retrieve all links and forms within a given site. 
Script logs links that are found (log_append()) and links that were searched already (log_done()).
The purpose of adding the SQLite aspect is to keep target domains links and form information in one place. Can be useful for later manipulation or validation of site changes if set on a scheduler. 

This script is not meant to be blazing fast. At the time of creation, it was just meant to work. 

Will be modifying as time and tasks permit. 

### Requirements
	- Pip -> requests_html -> pip3 install requests_html
	- SQLite -> https://www.sqlite.org/download.html
	- Directory folder -> DB (in same directory as script) -> holds sqlite DB

### Script Flow
1. Pass url -> http/s prefix not necessary -> applies https 
2. Loop through pages using links starting from home page (/)
	- Get rendered pages to have javascript forms applied
4. Get Forms -> Import into DB
5. Get Links -> for discovering new pages 
	- Loop through discovered links to verify if destination was found before. 
		- If not, add to master list 
		- Import discovered link into DB


### Output file Functions: 
log_append()-> appends discovered link to file -> useful for checking how many links were collected and are to be assessed. 
log_done() -> Logs finished page to file -> useful for checking which pages are done. 
