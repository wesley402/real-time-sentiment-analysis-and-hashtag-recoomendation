import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from nltk.tokenize import WordPunctTokenizer
from bs4 import BeautifulSoup
import re

plt.style.use('fivethirtyeight')

cols = ['sentiment','id','date','query_string','user','text']
df = pd.read_csv("sentiment140.csv",header=None, names=cols,sep=',', encoding='ISO-8859-1')
#df = pd.read_csv("training.1600000.processed.noemoticon.csv",header=None, names=cols,sep=',', encoding='latin-1')

#print(df.head())
#df.info()
#print(df.sentiment.value_counts())
# df.query_string.value_counts()
df.drop(['id','date','query_string','user'],axis=1,inplace=True)
print(df.head())
df[df.sentiment == 0].head(10)
df[df.sentiment == 4].head(10)
df['sentiment'] = df['sentiment'].map({0: 0, 4: 1})
print(df.sentiment.value_counts())


tok = WordPunctTokenizer()
pat1 = r'@[A-Za-z0-9]+'
pat2 = r'https?://[A-Za-z0-9./]+'
combined_pat = r'|'.join((pat1, pat2))

def tweet_cleaner(text):
    soup = BeautifulSoup(text, 'lxml')
    souped = soup.get_text()
    stripped = re.sub(combined_pat, '', souped)
    try:
        clean = stripped.decode("utf-8-sig").replace(u"\ufffd", "?")
    except:
        clean = stripped
    letters_only = re.sub("[^a-zA-Z]", " ", clean)
    lower_case = letters_only.lower()
    # During the letters_only process two lines above, it has created unnecessay white spaces,
    # I will tokenize and join together to remove unneccessary white spaces
    words = tok.tokenize(lower_case)
    return (" ".join(words)).strip()

nums = [0,400000,800000,1200000,1600000]

print("Cleaning and parsing the tweets...\n")
clean_tweet_texts = []
for i in range(nums[0],nums[1]):
    #if( (i+1)%10000 == 0 ):
     #   print("Tweets %d of %d has been processed" % ( i+1, nums[1] ))
    clean_tweet_texts.append(tweet_cleaner(df['text'][i]))
print(len(clean_tweet_texts))
for i in range(nums[1],nums[2]):
    #if( (i+1)%10000 == 0 ):
     #   print("Tweets %d of %d has been processed" % ( i+1, nums[1] ))
    clean_tweet_texts.append(tweet_cleaner(df['text'][i]))
print(len(clean_tweet_texts))
for i in range(nums[2],nums[3]):
    #if( (i+1)%10000 == 0 ):
     #   print("Tweets %d of %d has been processed" % ( i+1, nums[1] ))
    clean_tweet_texts.append(tweet_cleaner(df['text'][i]))
print(len(clean_tweet_texts))
for i in range(nums[3],nums[4]):
    #if( (i+1)%10000 == 0 ):
     #   print("Tweets %d of %d has been processed" % ( i+1, nums[1] ))
    clean_tweet_texts.append(tweet_cleaner(df['text'][i]))
print(len(clean_tweet_texts))
clean_df = pd.DataFrame(clean_tweet_texts,columns=['text'])
clean_df['target'] = df.sentiment
print(clean_df.head())
clean_df.to_csv('sentiment140_clean.csv',encoding='utf-8')
# csv = 'clean_tweet.csv'
# my_df = pd.read_csv(csv,index_col=0)
# print(my_df.head())