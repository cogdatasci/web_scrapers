# -------------------------------------------------------------------------------
# Name: Reddit_Data_Scraper.py
# Purpose: Pull data from Reddit
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

import pandas as pd
# from pandas_datareader import data
import requests
import praw
import time
import sys
from datetime import datetime
from praw.models import MoreComments

reddit = praw.Reddit(client_id="",
                    client_secret="",
                    redirect_uri="http://localhost:8888",
                    user_agent="")
print(reddit.auth.url(["identity"], "...", "permanent"))

def submissions_pushshift_praw(subreddit, start=None, end=None, limit=1000, extra_query=""):
    matching_praw_submissions = []

    # Default time values if none are defined (credit to u/bboe's PRAW `submissions()` for this section)
    utc_offset = 28800
    now = int(time.time())
    start = max(int(start) + utc_offset if start else 0, 0)
    end = min(int(end) if end else now, now) + utc_offset
    # extra_query = 'science'

    # Format our search link properly.
    search_link = ('https://api.pushshift.io/reddit/submission/search/'
                   '?subreddit={}&after={}&before={}&sort_type=created_utc&sort=asc&limit={}&q={}')
    search_link = search_link.format(subreddit, start, end, limit, extra_query)

    # Get the data from Pushshift as JSON.
    retrieved_data = requests.get(search_link)
    # print(retrieved_data.json())
    returned_submissions = retrieved_data.json()['data']

    # Iterate over the returned submissions to convert them to PRAW submission objects.
    for submission in returned_submissions:
        # Take the ID, fetch the PRAW submission object, and append to our list
        praw_submission = reddit.submission(id=submission['id'])
        matching_praw_submissions.append(praw_submission)

    # Return all PRAW submissions that were obtained.
    return matching_praw_submissions


# ******************************************* START ********************************************* #

arg = (sys.argv)
subredditid, query, start, end = arg[1:]

def get_time(t):
    import datetime
    date_format = datetime.datetime.strptime(t, "%m/%d/%Y,%H:%M:%S")
    return int(datetime.datetime.timestamp(date_format))


start_date = get_time(start)
end_date = get_time(end)


posts = pd.DataFrame(columns=['title', 'score', 'upvote_ratio', 'id',
                              'subreddit', 'url', 'num_comments', 'comments', 'body', 'created'])  # Dataframe to store results

comments_table = pd.DataFrame(columns=['id', 'author', 'author_id','subreddit', 'comment', 'created'])  # Dataframe to store comments

while start_date < end_date:  # Continue loop until end date is reached
    S = submissions_pushshift_praw(subreddit= subredditid,
                                   start=start_date, end=end_date, extra_query=query)  # Pull posts within date range
    for post in S:  # Looping through each post
        try:  # Try/except to catch any erroneous post pulls
            if post.selftext != '[removed]' and post.selftext != '[deleted]':  # Remove the deleted posts
                    submission = reddit.submission(id=post.id)
                    comments = []
                    for top_level_comment in submission.comments.list():
                        # print('start',top_level_comment)
                        if isinstance(top_level_comment, MoreComments):
                            continue
                        r = top_level_comment.author
                        redditor_id = reddit.redditor(r)
                        comment_id = top_level_comment.id
                        created = top_level_comment.created_utc
                        comments.append(top_level_comment.body)

                        comments_table = comments_table.append(
                        {
                            'id': top_level_comment.id,
                            'author': top_level_comment.author,
                            'author_id': redditor_id.id,
                            'subreddit': post.subreddit,
                            'comment': top_level_comment.body,
                            'created': str(datetime.fromtimestamp(created)),
                        }, ignore_index=True)
                        # print(comments_table)

                    posts = posts.append(
                        {'title': post.title,
                         'score': post.score,
                         'upvote_ratio': post.upvote_ratio,
                         'id': post.id,
                         'subreddit': post.subreddit,
                         'url': post.url,
                         'num_comments': post.num_comments,
                         'comments': comments,
                         'body': post.selftext,
                         'created': post.created}, ignore_index=True)  # Retrieve post data and append to dataframe
                    # print(posts)
        except:
            continue
            # next()   Continue loop if error is founD

    if len(S) < 100:  # To identify when the last pull is reached
        break

    start_date = posts['created'].max()  # Select the next earliest date to pull posts from
    print(start_date)  # An indicator of progress


comments_table['created'] = pd.to_datetime(posts['created'],unit='s')
posts['created'] = pd.to_datetime(posts['created'],unit='s')  # Converting Unix time to human readable
comments_table.to_csv('reddit_data_comments.csv', index=False)  # Export data to .csv file
posts.to_csv('reddit_data.csv', index=False)  # Export data to .csv file