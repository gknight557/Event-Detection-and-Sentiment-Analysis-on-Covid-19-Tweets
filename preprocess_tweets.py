import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob

"""
This program performs all pre-processing steps:
- Remove stop words
- Remove retweets
- Remove duplicate tweets
- Remove URLs and special characters
"""

path = "data\events\March\mar_23\march_23.csv"
df = pd.read_csv(path, usecols=['id','created_at','text'], encoding='utf-8')

# Text column needs to be formatted to fix issues with reading the data
#df['text'] = df['text'].apply(lambda x: x.encode('ascii', 'ignore').decode('ascii'))
# Convert created_at to pandas date-time format
df['created_at'] = pd.to_datetime(df['created_at'].astype('datetime64[ns]'))

print(df['text'].head())

# Remove all tweets which contain 'RT' - indicating a retweet
df = df[~df['text'].str.contains('RT', na = False)]

# English stopwords from NLTK package
stop_words = stopwords.words('english')
# Stop words extended to include collection words
stop_words.extend(['Covid19UK', 'CovidUK', 'Lockdownuk','Coronavirusuk','RT','covid19uk', 'coviduk', 'lockdownuk','coronavirusuk','COVIDUK','COVID19', 'rt'])

## PRE PROCESSING ##
"""
Removes any URLs and punctuation (or any special characters)

Args:
txt : (String)
"""
def remove_url(txt):
    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", txt).split())

"""
Returns a list of words after removing stop words
(Returns word (w) for each word in list if word not in stop word)

Args:
texts : (list) list of tokens
"""
def remove_stopwords(texts):
    # Tokenise tweet using NLTK tokenise method
    texts = word_tokenize(texts)
    # Return each word in the text if it is NOT present in the stopwords
    tokens_without_sw = [word for word in texts if not word in stop_words]
    # Join sentence back up separating each word with a space
    filtered_tweet = (" ").join(tokens_without_sw)
    # Return the filtered tweet with no stop words
    return filtered_tweet

# Apply preprocessing steps to text column
df['text'] = df['text'].apply(lambda x: remove_url(str(x)))
df['text'] = df['text'].apply(remove_stopwords)

# Drop any remaining duplicate tweets
df = df.drop_duplicates(subset=['text'])

# Export clean tweet dataframe to csv
#df.to_csv('clean_****.csv')
print(df['text'].head())
