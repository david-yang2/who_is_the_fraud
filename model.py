




def create_label(df):




    #add a new column called "Fraud"
    #True if any acct_type field contains the word fraud
    #False if it does not contain it
    #converted True to 1 and False to 0
    df["Fraud"] = df.acct_type.str.contains("fraud", regex = True).astype(int)

    #this will be our target
    label = df["Fraud"]

    return df