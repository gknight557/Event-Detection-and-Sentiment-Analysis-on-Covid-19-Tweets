from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import re
import nltk
from nltk.corpus import stopwords
from collections import Counter

"""
This program takes the tweets and returns a graph showing the counts of the different POS tags
 which is used to evaluate which tags are most commonly used within a collection of tweets
"""

"""
# IF USING TWEETS STRAUGHT FROM MONGO
client = MongoClient("mongodb://localhost:27017", unicode_decode_error_handler='ignore')
db = client.tweets_db

collection = db.tweets_collection

cursor = collection.find({"created_at": {"$regex" : ".*Feb 28.*"}} , projection=['text'], allow_disk_use=True)
tweet_fields = ['text']
df = pd.DataFrame(list(cursor), columns = tweet_fields)
"""

"""
# IF USING TWEETS FROM CSV
path = ""
df = pd.read_csv(path, usecols=['text'], encoding='utf-8')
"""

# Format text column to fix issues with reading data from column
df['text'] = df['text'].apply(lambda x: x.encode('ascii', 'ignore').decode('ascii'))

# English stopwords from nltk package
stop_words = stopwords.words('english')
# Stop words extended to include collection words
stop_words.extend(['covid19uk', 'coviduk', 'lockdownuk','coronavirusuk','rt'])

## PRE PROCESSING ##
"""
Removes any URLs and punctuation (or any special characters)

Args:
txt : (String)
"""
def remove_url(txt):
    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", txt).split())

"""
Returns string in all lower case

Args:
txt : (String) sentence to be uncapitalised
"""
def lower_case(txt):
    return txt.lower()

"""
Returns a list of words after removing stop words
(Returns word (w) for each word in list if word not in stop word)

Args:
texts : (string) string which will be tokenised and stopwords removed
"""
def remove_stopwords(text):
    text = text.split()
    return [w for w in text if not w in stop_words]

# Apply pre=processing functions to dataframe
df['text'] = df['text'].apply(lambda x: remove_url(x))
df['text'] = df['text'].apply(lambda x: lower_case(x))
df['text'] = df['text'].apply(remove_stopwords)

"""
Converts setence into a list of tuples and associated pos tag : (word, POS_tag)
Returns list of tags only with words removed

Args:
text : (String) Sentence to be tokenised
"""
def token_to_pos(text):
    pos_tokens = nltk.pos_tag(text)
    list = [tuple[1] for tuple in pos_tokens]
    return list

# Apply tokenisation and tagging to dataframe
df['text'] = df['text'].apply(token_to_pos)
# Apply counter function to each item in dataframe, converts into list of counts of each pos tag
df['text'] = df['text'].apply(lambda x: Counter(x))

# Converts text column to list - this results in a list of all POS tags, each tag representing the word in a tweet
data = df.text.values.tolist()
# Sums the POS tags using counter object
data = sum(data, Counter())
# Gets values for names and values, these being the names of the POS tags and the counts of each one
names, values = zip(*data.most_common(6))

# Plot the names and values in a bar chart
plt.bar(names, values)
# Add axis labels to graph
plt.xlabel('POS Tag')
plt.ylabel('Count of POS tag')
plt.show()
