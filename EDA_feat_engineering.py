import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from datetime import datetime
import re
import string
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

#read in the data
data = pd.read_json("data/data.json")

def clean_description(df):

    #remove HTML tags from each event's description
    #store it in a new column called "parsed_desc"
    df['parsed_desc'] = ""
    for n in range(df.shape[0]):
        soup = BeautifulSoup(df.description.iloc[n]).text.replace("\xa0", " ").replace("\n", " ").lower()
        df["parsed_desc"].iloc[n] = soup
    
    #remove punctuation and stopwords for each event and store it in
    #column called "parsed_desc_no_punc_or_stops"
    df["parsed_desc_no_punc_or_stops"] = ""
    for i in range(df.shape[0]):
        desc_no_punc_or_stops = []
        doc = df.parsed_desc.iloc[i]\
                    .translate(str.maketrans('', '', string.punctuation))
        for word in doc.split():
            if word not in stop_words:
                desc_no_punc_or_stops.append(word)
        
        df.parsed_desc_no_punc_or_stops.iloc[i] = ' '.join(desc_no_punc_or_stops)
    
    return df

def add_features(df):


    #did the get paid via ACH or check?
    #create dummies for the payout type
    payout_type = pd.get_dummies(df.payout_type)

    #combine the 2 dataframes
    df = df.join(payout_type)

    #the event_created, event_end, event_published, event_start
    #are shown in epoch time.
    #let's convert it to standard dates
    df["date_created"] = pd.to_datetime(df.event_created, unit='s').dt.date
    df["date_published"] = pd.to_datetime(df.event_published, unit='s').dt.date
    df["start"] = pd.to_datetime(df.event_start, unit='s').dt.date
    df["end"] = pd.to_datetime(df.event_end, unit='s').dt.date


    #e-mail domain feature
    #free e-mail domains
    #list of domains were found online
    free_domains = ["aol.com", "att.net", "comcast.net", "facebook.com", \
                    "gmail.com", "gmx.com", "googlemail.com", "google.com", \
                    "hotmail.com", "hotmail.co.uk", "mac.com", "me.com", \
                    "mail.com", "msn.com","live.com", "sbcglobal.net", \
                    "verizon.net", "yahoo.com"]
    #check to see if email domain for each event can be created for free
    free_email = df.email_domain.isin(free_domains)
    #convert to np array, so we can create a DataFrame
    email = free_email.values
    email_type = pd.DataFrame(email.reshape(-1,1))
    #rename the column
    email_type.columns = ['free_email']
    #combine the two dataframes
    df = df.join(email_type)

    #using the previous function to clean up the description feature
    df = clean_description(df)

    #replace NaNs in column has_header with 0
    df.has_header = df.has_header.fillna(value = 0)
    
    return df
    
def top_word_combo(df, min = 0.005, max = 0.5, features = 20):

    #create a corpus of all parsed descriptions
    corpus = df.parsed_desc.tolist()
    #instantiate TfidfVectorizer
    vectorizer = TfidfVectorizer(ngram_range = (2,2),\
                                min_df=min, \
                                max_df=max, \
                                max_features=50, \
                                stop_words ="english",\
                                token_pattern='\S+')
    tfidf = vectorizer.fit_transform(corpus)

    #convert into a matrix
    #identifying the top features
    sort_feat = np.argsort(tfidf.toarray()).flatten()[::-1]

    #array of feature names
    feat_names = np.array(vectorizer.get_feature_names())

    #top features we want to incorporate into our model
    top_features = feat_names[sort_feat][:features]

    #create a dataframe of the tfidf vector
    tfidf_vect = pd.DataFrame(tfidf.toarray(), \
                            columns = vectorizer.get_feature_names())
    #combine the 2 data frames
    df = df.join(tfidf_vect)

    return df