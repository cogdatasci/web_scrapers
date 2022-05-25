# Web_Scrapers

<b>********* Reddit Data Scraper ************</b>
1. Clone the files to the local system from the repository from master repo
2. Run the command `pip/pip3 install -r requirements.txt` (This installs the packages required by the python file to run)
3. Refer the following instructions to create an app and generate the keys required for the reddit scrapper: 
       <br> — Create a reddit account 
       <br> — Go to user settings
       <br> — Navigate to Safety & Privacy 
       <br> — Click on Manage third-party app authorization 
       <br> — Select Create an App - Give it a name, keep the other default values as such. Give a redirect uri (http://localhost:8080 could be a simple one to use) 
       <br> — To identify the ID and the secret refer [Reference](https://rymur.github.io/setup#:~:text=Redirect%20URI%3A%20The%20URI%20that,to%20when%20authenticating%20the%20user.)
       <br> — To understand how the keys would look, refer this page [OAuth](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example) 
	
4. Fill the respective keys in the file Reddit_Data_Scraper.py
5. Navigate to the current directory through terminal
6. Run the following command: `python3 Reddit_Data_Scraper.py ’Subreddit_id’ ‘Query’ ‘Start Date’ ‘End Date’`  (Start and end date are of the format —> mm/dd/yyyy,hh:mm:ss)
       Example command: `python3 DIY screwdriver 12/01/2021,00:00:00 01/02/2022,23:59:00` (DIY - subreddit id, screwdriver - query)
	<br>**Note:** 
	<br> — Try to give the duration of at least a month to fetch enough number of Reddits </ul>
        <br> — Subreddit id is of the form - r/subreddit_id (for a particular page) </ul>
        <br> — Query could be a string to filter out contents related to it </ul>
7. The execution generates 2 csv files in the current directory (reddit_data.csv and reddit_data_comments.csv)
8. After running the Reddit_Data_Scraper.py, run <b>Push_Data.py</b> to push the data scraped to the database
9. Fill the credentials in Push_Data.py received from the secure password management tool
10. Run the commmand `python3 Push_Data.py` in the terminal and monitor the console for response
11. After the completion of the process, you will observe - <b>Process Complete</b> message


