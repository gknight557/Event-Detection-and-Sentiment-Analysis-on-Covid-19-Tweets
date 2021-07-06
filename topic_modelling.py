from pymongo import MongoClient
import nltk
from nltk.corpus import stopwords
import re
import pandas as pd
import gensim
import gensim.corpora as corpora
import matplotlib.pyplot as plt
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from pprint import pprint

"""
This program takes an input from a csv file or straight from mongo and produces a topic model using the gensim LDA model
The topic outputs can then be written to a text file
"""

"""
# FOR USING TWEETS STRAIGHT FROM DB
client = MongoClient("mongodb://localhost:27017", unicode_decode_error_handler='ignore')
db = client.tweets_db

collection = db.tweets_collection

cursor = collection.find({"created_at": {"$regex" : ".*Jan 22.*"}}, projection=['text'], allow_disk_use=True)
tweet_fields = ['text']
df = pd.DataFrame(list(cursor), columns = tweet_fields)
"""

#"""
# FOR USING TWEETS FROM CSV
path = "data/past_tweets/ready_march20_21.csv"
df = pd.read_csv(path, usecols=['text'], encoding='utf-8')
#"""
# English stopwords from NLTK package
stop_words = stopwords.words('english')
# Stop words extended to include collection words
stop_words.extend(['corona','Covid19UK', 'CovidUK', 'Lockdownuk','Coronavirusuk','RT','covid19uk', 'coviduk', 'lockdownuk','coronavirusuk','COVIDUK','covid19'])

# Convert all tweets in text column to a list
# ['tweet','tweet',...]
data = df.text.values.tolist()

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
    return [word.lower() for word in txt]

"""
Returns a list of words after removing stop words
(Returns word (w) for each word in list if word not in stop word)

Args:
texts : (list) list of tokens
"""
def remove_stopwords(texts):
    return [w for w in texts if not w in stop_words]

"""
Pre processing of text:
Removes special characters from string then tokenises sentence and uncapitalises all words
"""
data = [remove_url(str(tweet)) for tweet in data]

tweet_tokens = [nltk.word_tokenize(tweet) for tweet in data]

tweet_tokens = [lower_case(word) for word in tweet_tokens]

"""
Making bigrams from common phrases
"""
# Phrases model automatically detects common phrases from a stream of sentences
# - In this case detecting bigrams
# min_count : Ignore all words and bigrams with total collected count lower than this value.
# threshold : Represent a score threshold for forming the phrases (higher means fewer phrases)
bigram = gensim.models.Phrases(tweet_tokens, min_count=5, threshold=50)
bigram_mod = gensim.models.phrases.Phraser(bigram)

"""
Uses the bigram model to detect bigrams
Reads each list of tweet tokens and passes into bigram model

Args:
texts: (list) list containing lists of tweet tokens
"""
def make_bigrams(texts):
    return [bigram_mod[tweet] for tweet in texts]

# # Passing tweet tokens into bigram model
tokens_bigrams = make_bigrams(tweet_tokens)
# Remove stopwords after bigrams have been made
tokens_bigrams_nsw = [remove_stopwords(tweet) for tweet in tokens_bigrams]

"""
LEMMATISATION
"""
# Empty list which will hold lemmatised words
data_lemmatized = []

# Initialise WordNet lemmatiser
WNlemma = WordNetLemmatizer()

"""
Simplifies given POS tag to one compatible with nltk lemmatize method.

Args:
tag : (String) given POS tag from nltk.pos_tag()

Returns: Wordnet pos tag. Default as NOUN if tag not applicable
"""
def get_wordnet_pos(tag):

    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

"""
List of tokens passed into pos_tag(), returns list of tuples [('token', 'TAG'), ... ]
For loop takes each tuple, returns compatible tag (pos), passes in token (tuple[0]) and tag to lemmatize method. Lemmatised word (lem)
appended to data_lemmatized.
"""
token_pos = [nltk.pos_tag(token_list) for token_list in tokens_bigrams_nsw]

for list in token_pos:
    list_lemmatiszed = []
    for tuple in list:
        pos = get_wordnet_pos(str(tuple[1]))
        lem = WNlemma.lemmatize(tuple[0], pos)
        list_lemmatiszed.append(lem)
    data_lemmatized.append(list_lemmatiszed)


"""
TOPIC MODEL
"""

"""
Each index needs to have its terms be in a sublist, all of which are nested within larger list.
e.g [['he', 'run'], ['eating', 'time']]
Dictionary object takes list of tokens and maps each word to a unique id
"""
dict = corpora.Dictionary(data_lemmatized)

# Create Corpus
texts = data_lemmatized

"""
doc2bow creates equivalent of document term matrix, gives mapping of (word_id, word_frequency)
"""
# Term Document Frequency
corpus = [dict.doc2bow(text) for text in texts]


"""
Build LDA model
"""
# corpus: Stream of document vectors or sparse matrix of shape
# id2word: Mapping from word IDs to words
# num_topics: number of requested latent topics to be extracted from the training corpus
# update_every: Number of documents to be iterated through for each update
# chunksize: Number of documents to be used in each training chunk
# passes: Number of passes through the corpus during training
# per_word_topics: If True, the model also computes a list of topics, sorted in descending order of most likely topics for each word
lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=dict,
                                           num_topics=5,
                                           update_every=1,
                                           chunksize=75,
                                           passes=100,
                                           per_word_topics=True)

# Print topics to console to see output
pprint(lda_model.print_topics())

"""
Write topic output to txt file
"""
# txt file path
path = ""
#f = open(path, 'w')
#f.write(str(lda_model.print_topics()))
#f.close()
