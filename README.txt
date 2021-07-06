All programs provided here are necessary to conduct the main analysis methods of this project.

Tweets should be taken from the data folder from any csv file provided.

The standard pre-processing of the tweets can be conducted using preprocess_tweets.py, although
many of the same pre-processing steps are present in most of the other programs - this just made it 
easier for quick testing on a dataset of tweets - these steps can be commented out as necessary within the 
other programs

A main overview of the programs provided is as follows:

Collecting tweets:
mongodb_connection: For collecting tweets from Twitter API and uploading to DB

twitter_credentials: twitter credentials for use in Twitter API

Pre-processing:
preprocess_tweets: for standard pre-processing of tweets - this includes removal of URLs, special characters
and stopwords as well as removal of retweets and duplicate tweets

mongo_to_event: extracting tweets from event timeframes

Analysis:
setiment: conducts sentiment analysis on tweets - i.e evaluate polarity and subjectivity values 

topic_modelling: Extract relevant topics from a collection of tweets

word_frequencies: Evaluate the most common words in a collection of tweets

pos_counter: Evaluate the most commonly used POS tags in a collection of tweets

max_tweets: Returns the maximum number of tweets collected within a 15 minute interval within a given day

Evaluation (using past data set of tweets):
ready_tweets: Formats tweet ID file from past dataset ready for use in tweet hydrator application

past_tweet_coordiante_filter: Filters tweets from past dataset to those only within a defined coordinate boundary
