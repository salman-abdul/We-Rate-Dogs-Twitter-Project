# We-Rate-Dogs-Twitter-Project
WeRateDogs is a Twitter account that rates people's dogs with a humorous comment about the dog. These ratings almost always have a denominator of 10. The numerators, though? Almost always greater than 10. 11/10, 12/10, 13/10, etc. Why? Because "they're good dogs Brent." WeRateDogs has over 4 million followers and has received international media coverage.

## Introduction
In this project, heterogeneous file resources and types were gathered, assessed and cleaned. And then stored as a one, ready-to-analyze master csv file, After that, some analysis was performed on that master cleaned csv file. The following is a summary of each phase

## GATHER

Data were gathered from three resources:

The first one was given as a csv file, namely twitter-archive-enhanced.csv, which was provided by WeRateDogs twitter account to Udacity and then to us. Then, the data was imported as a pandas dataframe twitter-archive. The second one was programmatically fetched from the URL https://d17h27t6h515a5.cloudfront.net/topher/2017/August/599fd2ad_image-predictions/image-predictions.tsv with which the response has been processed and saved into a tsv file, namely image-predictions.tsv. Then, the data was imported as a pandas dataframe image-predictions. The third one was through Twitter API, we fetched the data of those tweets we have and then saved them as a JSON file with UTF-8 encoding, namely tweet-json.txt, Then, the data was extracted as a pandas dataframe tweet-info. Assess Two types of assessments were performed, visual assessment and programmatic assessment. And the following issues were found:

## ASSESS
After gathering each of the above pieces of data, assess them visually and programmatically for quality and tidiness issues. Detect and document at least eight (8) quality issues and two (2) tidiness issues in your wrangle_act.ipynb Jupyter Notebook. To meet specifications, the issues that satisfy the Project Motivation (see the Key Points header on the previous page) must be assessed.

### TIDINESS

-there are too many dog species columns in twitter_archive, make it into one columns.

-merge data frame image_twitter, twitter_data and twitter_archive into one dataframe.


### QUALITY

#### twitter_archive:

-columns in_reply_to_status_id, in_reply_to_user_id, retweeted_status_id, retweeted_status_user_id convert datatype from 
float into string. 

-columns timestap and retweeted_status_timestamp convert datatype from object to datetime

-found invalid values in 'rating_numerator' and 'rating_denominator' : 0, 1770, 170.

-invalid name found in column 'name' : None, a, the, such, an.

-there are 50 missing value in column 'expanded url'.

-the last content in columns text is not readable, make it readable.

#### tweet_data:

-25 are missing in tweet_id

##### twitter_archive and image_twitter :

-drop columns jpg url and sources because they are less readable.

## CLEAN

All the issues mentioned in the assessment phase were resolved programmatically. For example, the four columns on the dog stage were merged into one column, some erroneous column data types were changed to the appropriate type, some invalid data were handled such as some invalid dog ratings found in the given data and so on. Finally, cleaned data files were merged as one file to make the data ready for analysis.

## ANALYSIS

After the data wrangling, we have ready-for-analysis data. We performed a quick analysis and elicitate some insights about it.






