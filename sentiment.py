from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob

"""
This program runs the sentiment check on tweets - tweets can be taken either straight from MongoDB or from a csv file
All preprocessing steps are run through and a plot is then displayed of the average values of polarity or subjectivity
 over 15 minute intervals
A csv file can be exported containing the preprocessed tweets along with added columns containing the sentiment values
"""

"""
# IF USING TWEETS STRAIGHT FROM DB
client = MongoClient("mongodb://localhost:27017", unicode_decode_error_handler='ignore')

db = client.tweets_db
collection = db.tweets_collection

cursor = collection.find({"created_at": {"$regex" : ".*Jan 12.*"}} , projection=['created_at','text'], allow_disk_use=True)
tweet_fields = ['created_at','text']
df = pd.DataFrame(list(cursor), columns = tweet_fields)
"""

#"""
# IF USING TWEETS FROM CSV
path = "data/past_tweets/ready_march21_22.csv"
df = pd.read_csv(path, usecols=['created_at','text'], encoding='utf-8')
#"""
# English stopwords from NLTK package
stop_words = stopwords.words('english')
# Stop words extended to include collection words
stop_words.extend(['Covid19UK', 'CovidUK', 'Lockdownuk','Coronavirusuk','RT','covid19uk', 'coviduk', 'lockdownuk','coronavirusuk','COVIDUK','COVID19'])

# Text column needs to be formatted to fix issues with reading the data
#df['text'] = df['text'].apply(lambda x: x.encode('ascii', 'ignore').decode('ascii'))
# Convert created_at to pandas date-time format
df['created_at'] = pd.to_datetime(df['created_at'].astype('datetime64[ns]'))

## PRE PROCESSING ##
"""
Removes any URLs and punctuation (or any special characters)

Args:
txt : (String)
"""
def remove_url(txt):
    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", txt).split())

"""
Returns word in all lower case

Args:
word : (String) word to be uncapitalised
"""
def lower_case(txt):
    return txt.lower()

"""
Returns a list of words after removing stop words
(Returns word (w) for each word in list if word not in stop word)

Args:
texts : (list) list of tokens
"""
def remove_stopwords(texts):
    texts = word_tokenize(texts)
    tokens_without_sw = [word for word in texts if not word in stop_words]
    filtered_sentence = (" ").join(tokens_without_sw)
    return filtered_sentence

# Apply pre-processing steps to text column of dataframe
df['text'] = df['text'].apply(lambda x: remove_url(str(x)))
#df['text'] = df['text'].apply(lower_case)
df['text'] = df['text'].apply(remove_stopwords)


"""
Runs sentiment check on tweet

Parameters
----------
tweet : string
    A text string of the database url

Returns
-------
List of polarity and subjectivity score for given tweet in format [polarity,subjectivity]
"""
def run_sentiment_check(tweet):
    # Tranforms tweet into text block compatible with TextBlob
    tb_text = TextBlob(tweet)
    # Compute polarity value
    # range [-1.0, 1.0]
    polarity = tb_text.sentiment.polarity
    # Compute subjectivity value
    # range [0.0, 1.0] 0 is objective, 1 is subjective
    subjectivity = tb_text.sentiment.subjectivity

    return [polarity,subjectivity]

# Empty polarity and subjectivity lists to be appended to dataframe
polarity = []
subjectivity = []

# Applies sentiment check to each tweet in text column
# Indexes in range of the length of the dataframe
for i in range(len(df.index)):
    # Index tweet in column and apply sentiment method
    # s - [polarity,subjectivity]
    s = run_sentiment_check(df['text'].loc[i])
    # Append polarity score to polarity list
    polarity.append(s[0])
    # Append subjectivity score to subjectivity list
    subjectivity.append(s[1])

# New polarity and subjectivity columns added through using list of values in pol and sub lists
df['polarity'] = polarity
df['subjectivity'] = subjectivity

# Can export dataframe to csv which now contains both sentiment values in columns
#df.to_csv('****.csv')

"""
Create plot of sentiment values over time
"""
# Create new df to plot values of by copying created_at and polarity/subjectivity columns to new df
# Uncomment either one to get plot of either polarity or subjectivity

#sentiment_time_df = df[['created_at', 'subjectivity']].copy()
sentiment_time_df = df[['created_at', 'polarity']].copy()

# Create group of average sentiment values over 15 minute intervals
group = sentiment_time_df.groupby(pd.Grouper(key='created_at',freq='15Min')).mean()

# Create plot and define figure size
group.plot.line(figsize=(18,7))

# Uncomment for correct ylabel description
#plt.ylabel('Average Subjectivity in 15 min intervals')
plt.ylabel('Average Polarity in 15 min intervals')

# Display graph
plt.grid(True)
plt.show()
