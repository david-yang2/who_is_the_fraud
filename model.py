from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix




def create_label(df):


    #add a new column called "Fraud"
    #True if any acct_type field contains the word fraud
    #False if it does not contain it
    #converted True to 1 and False to 0
    df["Fraud"] = df.acct_type.str.contains("fraud", regex = True).astype(int)

    #this will be our target
    label = df["Fraud"]

    return df, label

def prediction(df, features):

    df, y = create_label(df)

    X = df[features]

    #split our data into train and test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.33)

    clf = RandomForestClassifier()
    clf.fit(X_train, y_train)
    predictions = clf.predict(X_test)

    return predictions

def score(predictions, actual):
    return accuracy_score(y_test, predictions)