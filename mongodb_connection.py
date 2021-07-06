from pymongo import MongoClient

from tweepy.streaming import StreamListener
from tweepy.auth import OAuthHandler
from tweepy.streaming import Stream

import twitter_credentials
import json

DB_URL = "mongodb://localhost:27017"
DB_CLIENT = "tweets_db"

"""
Retrieves database client through local host server

Parameters
----------
url : string
    A text string of the database url

database : string
    A text string of the databse client within the server

Returns
-------
Database from local host server
"""
def get_db(url, database):

    client = MongoClient('localhost', 27017)
    return client['tweets_db']

"""
Uploads indiviudal tweet to database client

Parameters
----------
data : string
    A text string of the database url

Returns
-------
Database from local host server
"""
def upload_db(data):

    db = get_db(DB_URL, DB_CLIENT)

    collection = db['tweets_collection']
    tweet = json.loads(data)

    collection.insert_one(tweet)

# # # # TWITTER STREAMER # # # #
"""
Class for streaming and processing live tweets.
"""
class TwitterStreamer():

    """
    This handles Twitter authentification and the connection to Twitter Streaming API

    Args:
    fetched_tweets_filename: (string) file name which tweets can be saved to
    hash_tag_list: (list) list of hastags to stream tweets from
    """
    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # Listener object
        listener = StdOutListener(fetched_tweets_filename)
        # Authenticator for connection using twitter_credentials
        auth = OAuthHandler(twitter_credentials.API_KEY, twitter_credentials.API_KEY_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords:
        stream.filter(track=hash_tag_list)


# # # # TWITTER STREAM LISTENER # # # #
class StdOutListener(StreamListener):
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    # Takes in data from the StreamListener and uploads to database with upload_db method
    def on_data(self, data):
        try:
            #"""
            # Print tweet output if wanted
            data = json.loads(data)
            print(data)
            #"""
            upload_db(data)
        except BaseException as e:
            #print("Error on_data %s" % str(e))
            return True
    # Error method
    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    # Authenticate using config.py and connect to Twitter Streaming API.
    tags = ["Covid19UK", "CovidUK", "lockdownuk",'CoronavirusUK','Covid']
    fetched_tweets_filename = "tweet.json"

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, tags)
