from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import nltk

"""
This program creates a plot of tweet frequency over time, and uses the plot to extract tweets
 that are during an event timeframe (where frequency > value of threshold)
No pre-processing steps are applied to these tweets
Event tweets can be exported to new csv file which can then be used for further analysis
"""

"""
# IF USING TWEETS STRAIGHT FROM DB
client = MongoClient("mongodb://localhost:27017", unicode_decode_error_handler='ignore')

db = client.tweets_db
collection = db.tweets_collection

cursor = collection.find({"created_at": {"$regex" : ".*Feb 08.*"}}, projection=['id','created_at','text'], allow_disk_use=True)
tweet_fields = ['id','created_at','text']
df = pd.DataFrame(list(cursor), columns = tweet_fields)
"""

"""
# IF USING TWEETS FROM CSV
path = ""
df = pd.read_csv(path, usecols=['created_at','text'])
"""

# Text column needs to be formatted to fix issues with reading the data
df['text'] = df['text'].apply(lambda x: x.encode('ascii', 'ignore').decode('ascii'))
# Convert created_at to pandas date-time format
df['created_at'] = pd.to_datetime(df['created_at'].astype('datetime64[ns]'))

# Tweet frequency grouped in 15 minute intervals
tweet_df_15min = df.groupby(pd.Grouper(key='created_at', freq='15Min', convention='start')).size()
# Plot df values
tweet_df_15min.plot.line(figsize=(18,7))

# Define value of threshold
THRESHOLD = 120
# Plot indication of threshold on graph
plt.axhline(y=THRESHOLD, color='r', linestyle='-')

# Get lines from graph
ax = plt.gca()
line = ax.lines[0]

"""
Extracting event tweets from plot (where frequency > threshold value)
"""
# Use lines to extract x and y data values from plot
ydata = list(line.get_ydata())
xdata = list(line.get_xdata())
# Empty lists which will hold the indexes from ydata and xdata lists where values are > than threshold
ydata_index = []
xdata_index = []

# Count acts as index for list
# Takes each y value from plot (which represents the frequency value) and takes note of index in count
# If the y value is greater than the threshold value then the index is appended to ydata_index
count = -1
for num in ydata:
    count = count + 1
    if num > THRESHOLD:
        # Appends index values of numbers over threshold
        ydata_index.append(count)

# Uses indexes from ydata_index to get dates/times from where tweets go over THRESHOLD
for index in ydata_index:
    xdata_index.append(xdata[index].strftime('%Y-%m-%d %X'))

# Tranform dates to pandas date-time format
xdata_index = pd.to_datetime(xdata_index)

# Display the frequency graph
plt.ylabel('Num of tweets in 15 min intervals')
plt.grid(True)
plt.show()

"""
Create new event dataframe which contains all tweets where the frequency is greater than threshold
"""
FIFTEENMIN = pd.Timedelta(minutes=15)
# Empty dataframe
eventdf = pd.DataFrame(columns=['id', 'created_at', 'text'])

# Use indexes to create mask to collect all tweets from dataframe that are between the times gathered where frequency > threshold
for i in range(len(xdata_index)):
    # Takes each time index and gets tweets where created_at is between index and index + 15 minutes
    # index + 15 minutes because each interval on graph is 15 minutes
    mask = ((df['created_at'] >= xdata_index[i]) & (df['created_at'] <= (xdata_index[i] + FIFTEENMIN)))
    # Assign mask to temp variable
    temp = df.loc[mask]
    # Append temp to event dataframe
    eventdf = eventdf.append(temp)

# Can export event dataframe to new csv for further analysis
#eventdf.to_csv('****.csv')
