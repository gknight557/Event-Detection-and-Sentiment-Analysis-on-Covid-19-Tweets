"""
For use with a past dataset of tweets.

Past dataset can be found here: https://ieee-dataport.org/open-access/coronavirus-covid-19-geo-tagged-tweets-dataset

csv file needs to be in right format for tweets to be hydrated

Takes csv file and exports tweet ID column to new csv file so it is compatible with the hydrator application
"""
import pandas as pd

# Read tweet ID csv file - taken straight from website above 
dataframe=pd.read_csv("data/past_tweets/march/march26_march27.csv", header=None)

# New dataframe conatining first column of csv (tweet IDs)
dataframe=dataframe[0]

# Export to new 'ready' csv file for use in hydrator
dataframe.to_csv("data/past_tweets/march/ready_march26_27.csv", index=False, header=None)
