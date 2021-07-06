import pandas as pd

"""
For use with past dataset of tweets
Prior to running this, the coordiante values need to be separated in excel and placed in long and lat columns
As the past dataset contains global tweets, the coordiantes are used to filter down the tweets to a more specific location
This program currently narrows down to tweets posted in the US

Compares coordiantes of tweets and appends to dataframe if its within the boundaries of the US coordiantes
"""
# csv file path
path = ""
df = pd.read_csv(path, usecols=['long','lat','created_at','place','text'])

df['created_at'] = pd.to_datetime(df['created_at'].astype('datetime64[ns]'))
df['text'] = df['text'].apply(lambda x: x.encode('ascii', 'ignore').decode('ascii'))

"""
Takes string of longitude value and checks if it is within longitude boundaries of US

Returns True if within boundary
"""
def long_in_us(string):
    long = float(string)
    if (-126.11240083879932 <= long <= -63.53427583879932):
        return True

"""
Takes string of latitude value and checks if it is within latitude boundaries of US

Returns True if within boundary
"""
def lat_in_us(string):
    lat = float(string)
    if (31.31402034710526 <= lat <= 43.96998199013549):
        return True

# Long and lat values to a list to be iterated through
long = df['long'].values.tolist()
lat = df['lat'].values.tolist()

# Empty lists - True will be appended to these lists if equivalent row in long and lat lists are within US coordinates
lo_list = []
la_list = []

# Check coordiantes for each long and lat value in long and lat lists
for l in long:
    lo_list.append(long_in_us(l))

for l in lat:
    la_list.append(lat_in_us(l))

# Add new dataframe columns containing True against each tweet if either long or lat is within US
df['long_in_us'] = lo_list
df['lat_in_us'] = la_list

# Export dataframe to new csv file
df.to_csv("****.csv")

"""
After running this code, all rows of tweets which do not have a True value in both long_in_us and lat_in_us need to be removed
- this is done seperately in excel
"""

"""
America lat,long
- Coordinates represent the coordinates of the 4 corners around the US
43.96998199013549, -126.11240083879932
43.96998199013549, -63.53427583879932
31.31402034710526, -63.53427583879932
31.31402034710526, -125.11240083879932
"""
