#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# -------------------------------------------------------------------------------
# Name: Twitter_Data_Scraper.py
# Purpose: Pull data from twitter
#
# Author(s):    Sharath Srikanth
#
# Created:      03/02/2022
# Updated:
# Update Comment(s):
#
# TO DO:
#
# -------------------------------------------------------------------------------


# In[1]:


# imports

import requests
import pandas as pd
import time
import regex as re
from datetime import datetime, timedelta


# In[2]:


# defining data object 

def get_data(tweet):
    data = {
        'id': tweet['id'],
        'author_id': tweet['author_id'],
        'created_at': tweet['created_at'],
        'text': tweet['text'],
        'retweet_count': tweet['public_metrics']['retweet_count'],
        'like_count': tweet['public_metrics']['like_count'],
        'reply_count': tweet['public_metrics']['reply_count'],
        'latitude': tweet['geo']['coordinates']['coordinates'][0],
        'longitude': tweet['geo']['coordinates']['coordinates'][1],
        'raw_data': tweet
    }
    return data


# In[3]:


# defining pattern matching to filter data to clean

whitespace = re.compile(r"\s+")
web_address = re.compile(r"(?i)http(s):\/\/[a-z0-9.~_\-\/]+")
user = re.compile(r"(?i)@[a-z0-9_]+")


# In[15]:


#------------------------------------- Twitter Data Pull  --------------------------------------------------------

# setup the API request
BEARER_TOKEN = ''
endpoint = 'https://api.twitter.com/2/tweets/search/all'
# endpoint = 'https://api.twitter.com/1.1/search/tweets.json'
headers = {'authorization': f'Bearer {BEARER_TOKEN}'}
params = {
    
    'max_results': '100',
    'tweet.fields': 'created_at,lang,public_metrics'
        }

# In[16]:


# formatting the date object for twitter data

dtformat = '%Y-%m-%dT%H:%M:%SZ'  # the date format string required by twitter

# we use this function to subtract 60 mins from our datetime string
def time_travel(now, mins):
    now = datetime.strptime(now, dtformat)
    back_in_time = now - timedelta(minutes=mins)
    return back_in_time.strftime(dtformat)


# In[17]:
now = datetime.now()  # get the current datetime, this is our starting point
last_week = now - timedelta(days=6)  # datetime one week ago = the finish line
now = now.strftime(dtformat)  # convert now datetime to format for API


# In[18]:
df = pd.DataFrame()  # initialize dataframe to store tweets

while True:
    if datetime.strptime(now, dtformat) < last_week:
        # if we have reached 6 days ago, break the loop
        break
    pre60 = time_travel(now, 5)  # get x minutes before 'now'
    
    # assign from and to datetime parameters for the API
    params['start_time'] = pre60
    params['end_time'] = now
    response = requests.get(endpoint,
                            params=params,
                            headers=headers)  # send the request
    print('response - ',response)
    time.sleep(2)
    now = pre60  # move the window 60 minutes earlier
    # iteratively append our tweet data to our dataframe
    for tweet in response.json()['data']:
        row = get_data(tweet)  # we defined this function earlier
        if row['like_count'] >= 0 and row['retweet_count'] >= 0 and row['reply_count'] >= 0:   #row['like_count'] >=3:
            df = df.append(row, ignore_index=True)

# print data frame

# logic to store the data




