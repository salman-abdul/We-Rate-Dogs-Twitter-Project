#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import requests
import tweepy
import json
import time
import os
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from tweepy import OAuthHandler
from timeit import default_timer as timer


# # GATHERING DATA 

# In[2]:


###  First Data
twitter_archive = pd.read_csv('twitter-archive-enhanced.csv')
# Showing the Data 
twitter_archive.head(2)


# In[3]:


### Second Data From Image
#Download the data from url link that already provided
tsv_url = ' https://d17h27t6h515a5.cloudfront.net/topher/2017/August/599fd2ad_image-predictions/image-predictions.tsv'
image_req = requests.get(tsv_url, allow_redirects=True)
open('image_predictions.tsv', 'wb').write(image_req.content)

#Showing the data:
image_twitter = pd.read_csv('image_predictions.tsv', sep = '\t')
image_twitter.head(2)


# In[4]:


#Third Data From Twitter API
# Query Twitter API for each tweet in the Twitter archive and save JSON in a text file
# These are hidden to comply with Twitter's API terms and conditions
consumer_key = 'bpCrEHSfzmOxrivBj3ZZSUeS2'
consumer_secret = 'wGJcz98kDRT7VOJs8iKndTWBzGQDUrtJQjvcu9QGtBi29VQocl'
access_token = '1347824265358282757-0QwFRk7ixb0yy4u3BVofX5vW2aV2b2'
access_secret = 'rFmU6dBrjeorOMpumujG2zPqhGCAVRxoJhr3M0SfB7XEq'
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)
api.me()


# In[5]:


# NOTE TO STUDENT WITH MOBILE VERIFICATION ISSUES:
# df_1 is a DataFrame with the twitter_archive_enhanced.csv file. You may have to
# change line 17 to match the name of your DataFrame with twitter_archive_enhanced.csv
# NOTE TO REVIEWER: this student had mobile verification issues so the following
# Twitter API code was sent to this student from a Udacity instructor
# Tweet IDs for which to gather additional data via Twitter's API
tweet_ids = twitter_archive.tweet_id.values
len(tweet_ids)

# Query Twitter's API for JSON data for each tweet ID in the Twitter archive
count = 0
fails_dict = {}
start = timer()
# Save each tweet's returned JSON as a new line in a .txt file
with open('tweet_json.txt', 'w') as outfile:
    # This loop will likely take 20-30 minutes to run because of Twitter's rate limit
    for tweet_id in tweet_ids:
        count += 1
        print(str(count) + ": " + str(tweet_id))
        try:
            tweet = api.get_status(tweet_id, tweet_mode='extended')
            print("Success")
            json.dump(tweet._json, outfile)
            outfile.write('\n')
        except tweepy.TweepError as e:
            print("Fail")
            fails_dict[tweet_id] = e
            pass
end = timer()
print(end - start)
print(fails_dict)


# In[6]:


tweet_json_file = 'tweet_json.txt'


# In[7]:


# read in the JSON data from the text file, and save to a DataFrame
tweet_json_data = []

with open(tweet_json_file, 'r') as json_file:
    # read the first line to start the loop
    line = json_file.readline()
    while line:
        data = json.loads(line)

        # extract variables from the JSON data
        data_id = data['id']
        data_retweet_count = data['retweet_count']
        data_favorite_count = data['favorite_count']
        
        # create a dictionary with the JSON data, then add to a list
        json_data = {'tweet_id': data_id, 
                     'retweet_count': data_retweet_count, 
                     'favorite_count': data_favorite_count
                    }
        tweet_json_data.append(json_data)

        # read the next line of JSON data
        line = json_file.readline()
        # ----- while -----

# convert the tweet JSON data dictionary list to a DataFrame
tweet_data = pd.DataFrame(tweet_json_data, 
                                   columns = ['tweet_id',
                                              'retweet_count',
                                              'favorite_count'])

tweet_data.head(5)


# Gather Data:
# 1. twitter_archive dataframe contains basic tweet info.
# 2. image_twitter daframe contains image from tweet.
# 3. tweet_data dataframe contains tweet information such as : tweet_id, retweet_count and favorite count.

# # ASSESS
# Note: issues found are documented at the end of the assessment section

# ### Visual Assessment

# In[8]:


twitter_archive.head(5)


# In[9]:


twitter_archive.tail(5)


# In[10]:


twitter_archive.columns


# In[11]:


twitter_archive.shape


# In[12]:


image_twitter.head(5)


# In[13]:


image_twitter.tail(5)


# In[14]:


image_twitter.columns


# In[15]:


image_twitter.shape


# In[16]:


tweet_data.head()


# In[17]:


tweet_data.tail()


# In[18]:


tweet_data.shape


# In[19]:


tweet_data.columns


# ### Programmatic Assessment

# In[20]:


twitter_archive.info()


# In[21]:


twitter_archive['retweeted_status_timestamp'].unique()


# In[22]:


twitter_archive.describe()


# In[23]:


twitter_archive.rating_numerator.value_counts()


# In[24]:


twitter_archive.rating_denominator.value_counts()


# In[25]:


twitter_archive.name.value_counts()


# In[26]:


#check if twitter_archive in column tweet id has duplicate value 
twitter_archive['tweet_id'].duplicated().sum()


# In[27]:


twitter_archive.in_reply_to_status_id.shape


# In[28]:


twitter_archive.in_reply_to_status_id.value_counts().sum()


# In[29]:


#check Nan values, it shows Nan values more than 80% of the row values so 
#we don't do anything because if we delete those Nan, we will short the data.
twitter_archive.isnull().sum()


# In[30]:


image_twitter.info()


# In[31]:


image_twitter.describe()


# In[32]:


image_twitter.tweet_id.duplicated().sum()
#There is no duplicate values


# In[33]:


image_twitter.isnull().sum()
#There is no Nan values


# In[34]:


tweet_data.info()


# In[35]:


tweet_data.describe()


# In[36]:


tweet_data.duplicated().sum()


# In[37]:


tweet_data.isnull().sum()


# In[38]:


twitter_archive.shape[0] - tweet_data.shape[0]


# ### Quality
# 
# #### From Visual assessment:
# 
# ##### twitter_archive and image_twitter :
# -drop columns jpg url and sources because they are less readable.
# 
# #### From Programmatic Assessment
# 
# #### twitter_archive:
# -columns in_reply_to_status_id, in_reply_to_user_id, retweeted_status_id, retweeted_status_user_id convert datatype from 
# float into string. 
# 
# -columns timestap and retweeted_status_timestamp convert datatype from object to datetime
# 
# -found invalid values in 'rating_numerator' and 'rating_denominator' : 0, 1770, 170.
# 
# -invalid name found in column 'name' : None, a, the, such, an.
# 
# -there are 50 missing value in column 'expanded url'.
# 
# -the last content in columns text is not readable, make it readable.
# 
# #### tweet_data:
# -25 are missing in tweet_id
# 
# 
# 
# 

# ### Tidiness
# -there are too many dog species columns in twitter_archive, make it into one columns.
# 
# -merge data frame image_twitter, twitter_data and twitter_archive into one dataframe.
# 

# # Clean

# In[39]:


twitter_archive_clean = twitter_archive.copy()
image_twitter_clean = image_twitter.copy()
tweet_data_clean = tweet_data.copy()


# In[40]:


twitter_archive_clean.columns


# ### Solving tidiness problem
# 
# #### Define 
# Merge the dog species into one columns['doggo', 'floofer', 'pupper', 'puppo'] and named the column 'dog_special'

# #### Code

# In[41]:


twitter_archive_clean['dog_special'] = twitter_archive_clean.text.str.extract('(puppo|pupper|floofer|doggo)', expand=True)
columns = ['doggo', 'floofer', 'pupper', 'puppo']
twitter_archive_clean = twitter_archive_clean.drop(columns, axis=1)
twitter_archive_clean.head()


# #### Test

# In[42]:


columns = ['pupper', 'doggo', 'puppo', 'floofer']
for col in columns:
    print(col, twitter_archive[col].value_counts()[1])


# In[43]:


twitter_archive_clean['dog_special'].value_counts()


# #### Define
# 
# -merge data frame image_twitter, twitter_data and twitter_archive into one dataframe

# #### Code

# In[44]:


twitter_archive_clean = pd.merge(twitter_archive_clean, image_twitter_clean, how='left', on='tweet_id')
twitter_complete = pd.merge(twitter_archive_clean,  tweet_data_clean, how='left', on='tweet_id')


# ### Test

# In[45]:


twitter_complete.sample(5)


# In[46]:


twitter_complete.columns


# ### Solving Quality Problem
# 
# #### Define 
# -drop columns source, and jpg_url  because they areless readable.

# #### Code

# In[47]:


twitter_complete.drop(['source', 'jpg_url'], axis = 1, inplace= True)


# #### Test

# In[48]:


twitter_complete.columns


# #### Define
# columns in_reply_to_status_id, in_reply_to_user_id, retweeted_status_id, retweeted_status_user_id convert datatype from 
# float64 into string. 
# 

# #### Code

# In[49]:


twitter_complete.in_reply_to_status_id = twitter_complete.in_reply_to_status_id.astype('str')
twitter_complete.in_reply_to_user_id = twitter_complete.in_reply_to_user_id.astype('str')
twitter_complete.retweeted_status_id = twitter_complete.retweeted_status_id.astype('str')
twitter_complete.retweeted_status_user_id = twitter_complete.retweeted_status_user_id.astype('str')


# In[50]:


#### Test 


# In[51]:


twitter_complete.dtypes


# #### Define
# -columns timestap and retweeted_status_timestamp convert datatype from object to datetime

# #### Code

# In[52]:


twitter_complete['timestap'] = pd.to_datetime(twitter_complete['timestamp']) 
twitter_complete['retweeted_status_timestamp'] = pd.to_datetime(twitter_complete['retweeted_status_timestamp']) 


# #### Test

# In[53]:


twitter_complete.dtypes


# #### Define
# -found invalid values in 'rating_numerator' and 'rating_denominator' : 0, 1770, 170. Discover the reason!

# #### Code

# In[54]:


twitter_complete['rating_numerator'].value_counts()


# In[55]:


twitter_complete['rating_denominator'].value_counts()


# As we can see, all 'rating_numerator' and 'rating_denominator' with counts less than or equal 3 are invalid, so this must be delete from the column.

# In[56]:


twitter_complete.rating_numerator.value_counts().loc[lambda x : x <= 3].sum()


# In[57]:


twitter_archive_clean.rating_denominator.value_counts().loc[lambda x : x <= 3].sum()


# we have 53 records with invalid rating, it is small portion, it won't affect this analyst, we just dropped it.

# In[58]:


numerators_delete = twitter_complete.rating_numerator.value_counts().loc[lambda x : x <= 3]
for numerator in numerators_delete.index:
    twitter_complete.drop(twitter_complete.query('rating_numerator == ' + str(numerator)).index, inplace=True)
    
denominator_delete = twitter_complete.rating_denominator.value_counts().loc[lambda x : x <= 3]
for denominator in denominator_delete.index:
    twitter_complete.drop(twitter_complete.query('rating_denominator == ' + str(denominator)).index, inplace=True)


# In[59]:


twitter_complete.rating_numerator.value_counts()


# In[60]:


#### Test


# In[61]:


twitter_complete.rating_numerator.value_counts()


# In[62]:


twitter_complete.rating_denominator.value_counts()


# #### Define
# -invalid name found in column 'name' : None, a, the, such, an. Change those into NaN

# #### Code

# In[63]:


twitter_complete.dog_special.head(10)


# It automatically changes when we merged the columns.

# #### Test

# In[64]:


twitter_complete.dog_special.isnull().sum()


# #### Define
# -there are 50 missing value in column 'expanded url'.
# 

# In[65]:


twitter_complete.columns


# #### Code

# In[66]:


twitter_complete['expanded_urls'].isna().sum().sum()


# In[67]:


twitter_complete.dropna(subset = ['expanded_urls'],inplace = True)


# #### Test 

# In[68]:


twitter_complete['expanded_urls'].isna().sum().sum()


# #### Define
# -25 are missing in tweet_id
# 
# twitter_complete.info()

# #### Code

# In[69]:


twitter_complete['tweet_id'].isna().sum().sum()


# In[70]:


#### Test


# In[71]:


twitter_complete['tweet_id'].isna().sum().sum()


# There are no missing value because when we merged the table, it already solved it for us

# #### Define
# -the last content in columns text is not readable, because the space is too narrow,  make it readable.

# #### Code 
# 

# In[72]:


twitter_complete.text.head()


# In[73]:


#Display all the text in the column
pd.set_option('display.max_colwidth', -1)


# #### Test

# In[74]:


twitter_complete.text.head()


# # Store

# In[75]:


twitter_complete.to_csv('twitter_master.csv', index=False)


# 
# 
# 

# # Analyze

# In[76]:


get_ipython().run_line_magic('matplotlib', 'inline')


# In[77]:


pd.set_option('display.max_columns', None)


# In[78]:


twitter_df = twitter_complete


# In[79]:


# We have to slice the unnecessary values in timestamp like hours, minutes and seconds. Also after that we sorted it from old to new.
twitter_df = twitter_complete.copy()
twitter_df.timestamp = twitter_df.timestamp.str[0:10]
twitter_df.timestamp
twitter_df = twitter_df.sort_values(by=['timestamp'])


# Let's check the retweet_count and likes over time

# In[80]:


df_time_indexed = twitter_df.set_index('timestamp')
df_time_indexed[['retweet_count', 'favorite_count']].plot(alpha=2.0, style='.')
plt.xlabel('timestamp')
plt.ylabel('count')
plt.savefig('retweets_favorites_over_time.png')
plt.title('Retweets and likes over time');


# #### We can see favorite count increase each year.

# In[81]:


twitter_df.head(1)


# In[82]:


df_time_indexed ['rating_ratio'] = df_time_indexed ['rating_numerator'] / df_time_indexed ['rating_denominator']
df_time_indexed ['rating_ratio'].plot(alpha=0.3, style='.')
plt.xlabel('timestamp')
plt.ylabel('rating ratio')
plt.savefig('ratings_over_time.png')
plt.title('Rating ratio over time');


# #### It shows rating ratio increases over time
# 

# In[83]:


twitter_df.head(2)


# Let's check if the p1, p2, p3 affect the rating ratios¶

# In[84]:


df_time_indexed.groupby('dog_special')['rating_ratio'].describe()


# 
# The means in the above table seem to indicate a low rating ratio for "pupper" dog stage, but that might be affected by the low outliers and high number of them, however, the medians also indicate the same thing, so the outliers are not the problem, therefore, we can conclude that the "pupper" dog stage tends to get less rating ratios.
# 
# The "floofer" dog stage gets the highest rating ratios among other stages, with always getting higher than 10 rating ratio, but that also might be due to the very few number of dogs at this stage.

# In[85]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'wrangle_act.ipynb'])


# In[ ]:




