import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from datetime import datetime
import re


#read in the data
data = pd.read_json("data/data.json")

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

    #what's in the description of each event?


    return df
    
