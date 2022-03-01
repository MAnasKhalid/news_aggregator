import praw as praw

# all these should come from config.py later
from mod_api.helpers import aggregator_map

CLIENT_ID = "h5-b4LSWCJNPUrIEy1Zwvw"
CLIENT_SECRET = "fnEfei-UCrl_Eqdj5uPJza4wzC3JlQ"
REDDIT_USERNAME = "AnasKhalid158"
REDDIT_PASSWORD = "facebook158"

# TODO:ENCAPSULATE ALL THESE IN REDDIT CLASS
# TODO: ALL THE SECRETS SHOULD BE IN INI FILE

def authenticate():
    # https://www.jcchouinard.com/get-reddit-api-credentials-with-praw/
    return praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        password=REDDIT_PASSWORD,
        user_agent="testscript by u/anaskhalid",
        username=REDDIT_USERNAME,
    )


def get_data(query, type='news', reddit=None):
    if reddit is None:
        return
    results = reddit.subreddit("news").search(query=query)
    data = []
    # https://praw.readthedocs.io/en/latest/code_overview/models/subreddit.html#
    for submission in results:
        data.append(aggregator_map(submission.url,submission.title,source='reddit'))
    return data
