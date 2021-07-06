import pandas as pd
import matplotlib.pyplot as plt
import re
import collections
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import gensim
import gensim.corpora as corpora

"""
This program calculates the most common words used in a collection of tweets
It returns a bar graph representation of the most common words - without stop or collection words
Pre-processing is applied to the tweets before hand to ensure all stop words, collection words and URLs are removed
Tweets are read directly from a csv file
"""

# csv file path
path = "data/events/February/feb_03/feb_03.csv"
df = pd.read_csv(path, usecols=['text'], encoding='utf-8')

# English stopwords from NLTK package
stop_words = stopwords.words('english')
# Stop words extended to include collection words
stop_words.extend(['Covid19UK', 'CovidUK', 'Lockdownuk','Coronavirusuk','RT','covid19uk', 'coviduk', 'lockdownuk','coronavirusuk','COVIDUK','COVID19','covid19','amp','coronavirus','covid','uk','19','lockdown'])

### PRE-PROCESSING ###
"""
Removes any URLs and punctuation (or any special characters)

Args:
txt :
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
tweet : (string) a single tweet as a string
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

"""
Removes any URLs and punctuation (or any special characters)

Args:
txt : (String)
"""
def remove_url(txt):
    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", txt).split())

# Apply pre-processing steps
df['text'] = df['text'].apply(lambda x: remove_url(str(x)))
df['text'] = df['text'].apply(lambda x: lower_case(str(x)))
df['text'] = df['text'].apply(remove_stopwords)

# Converts all tweets in text column to list of tweets
# ['full tweet','full tweet',....]
all_tweets = df['text'].tolist()

# Splits each full tweet in list into a list of tokens
# [['token','token''token'],['token','token''token'],...]
# Input for gensim phrases must be a list of string tokens
all = [tweet.split() for tweet in all_tweets]

"""
Making bigrams from common phrases
"""
# Phrases model automatically detects common phrases from a stream of sentences
# - In this case detecting bigrams
# min_count : Ignore all words and bigrams with total collected count lower than this value.
# threshold : Represent a score threshold for forming the phrases (higher means fewer phrases)
bigrams = gensim.models.Phrases(all, min_count=1, threshold=20)
bigram_model = gensim.models.phrases.Phraser(bigrams)

"""
Uses the bigram model to detect bigrams
Reads each list of tweet tokens and passes into bigram model

Args:
texts: (list) list containing lists of tweet tokens
"""
def make_bigrams(texts):
    return [bigram_model[tweet] for tweet in texts]

# Passing tweet tokens into bigram model
tokens_bigrams = make_bigrams(all)

all_words = []

# Separting lists into single list
# For each list of tokens_bigrams, append each token to all_words list
for tweet in tokens_bigrams:
    for word in tweet:
        all_words.append(word)

# Create counter for all words
word_counter = collections.Counter(all_words)

# Takes top 15 most words from word counter and passes into new dataframe which will be used to make plot
word_count_df = pd.DataFrame(word_counter.most_common(15), columns=['words', 'count'])

# Sort words by highest to lowest counts
word_count_df = word_count_df.sort_values(by='count')

# Plot results in bar graph
plot = word_count_df.plot.barh(x='words', y='count', color="purple", figsize=(14,8))

# Set title of graph
plt.title("Common Words Found in Tweets (Without Stop Words or Collection Words)")

# Display graph
plt.show()

"""
Save figure
"""
fig = plot.get_figure()
# Path to save figure
path = "***.png"
#fig.savefig(path)
