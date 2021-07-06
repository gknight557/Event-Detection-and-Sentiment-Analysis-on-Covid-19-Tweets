from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt

"""
This program returns a list of the max number of tweets returned within a 15 minute interval on a given day
"""

# Get tweets straight from MongoDB
client = MongoClient("mongodb://localhost:27017", unicode_decode_error_handler='ignore')
db = client.tweets_db

collection = db.tweets_collection

# Empty list which will contain the values of the max number of tweets each day
max_tweet = []
# Dates to index through - add more as needed
dates = ['11', '12']

for date in dates:
    # Get tweets for date in dates list
    cursor = collection.find({"created_at": {"$regex" : ".*Mar " + date + ".*"}} , projection=['created_at','text'], allow_disk_use=True)

    tweet_fields = ['created_at','text']
    df = pd.DataFrame(list(cursor), columns = tweet_fields)

    df['text'] = df['text'].apply(lambda x: x.encode('ascii', 'ignore').decode('ascii'))
    df['created_at'] = pd.to_datetime(df['created_at'].astype('datetime64[ns]'))

    # Create 15 minute plot
    tweet_df_15min = df.groupby(pd.Grouper(key='created_at', freq='15Min', convention='start')).size()
    tweet_df_15min.plot.line(figsize=(18,7))

    # Get lines from plot
    ax = plt.gca()
    line = ax.lines[0]

    # Get y values from plot
    ydata = list(line.get_ydata())
    # Append the max value from all frequency values of ydata
    max_tweet.append(max(ydata))
    # Clear figure for next round in for loop
    plt.clf()
# Print list of max values
print(max_tweet)
