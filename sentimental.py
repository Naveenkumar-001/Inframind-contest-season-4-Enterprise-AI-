# -*- coding: utf-8 -*-
"""sentimental.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wiChTPgF4slSjT_k7qobCmabMdjFsdH8
"""

import pandas as pd
data=pd.read_csv('train.csv')
data.head()
# Data credit - https://www.kaggle.com/anu0012/hotel-review?select=test.csv

data.shape

data.info()

data.describe().transpose()

"""**Data Cleaning / EDA**"""

#checking missing values in the data set and printing the percentage for missing values for each columns

count=data.isnull().sum().sort_values(ascending=False)
percentage=((data.isnull().sum()/len(data)*100)).sort_values(ascending=False)
missing_data=pd.concat([count,percentage],axis=1,
keys=['Count','Percentage'])
print('Count and percentage of missing values for the coulumns: ')
missing_data

# Commented out IPython magic to ensure Python compatibility.
#checking for thee distribution of dafault

import matplotlib.pyplot as plt
# %matplotlib inline
print('Percentage for default\n')
print(round(data.Is_Response.value_counts(normalize=True)*100,2))
round(data.Is_Response.value_counts(normalize=True)*100,2).plot(kind='bar')
plt.title('Percentage Distribution by review type')
plt.show()

#Removing columns
data.drop(columns=['User_ID','Browser_Used','Device_Used'],inplace=True)

#Apply first level cleaning

import re
import string
#This function converts to lower case,removes square brackeets,remove numbers and punctuation
def text_clean_1(text):
    text=text.lower()
    text = re.sub('\[.*?\]', '', text) 
    text = re.sub( '[%s]' % re.escape(string.punctuation), '',text)

    text = re.sub('w\d\w*', '' , text)


    return text

cleaned1 =lambda x: text_clean_1(x)

#let take a look at the updated text
data['cleaned_description'] = pd.DataFrame(data.Description.apply(cleaned1))
data.head(10)

#apply second round of cleaning
def text_clean_2(text):
  text = re.sub('[''""...]','',text)
  text = re.sub('\n', '', text)
  return text 

cleaned2 = lambda x: text_clean_2(x)

#lets take look at the updated text
data['cleaned_description_new'] = pd.DataFrame(data['cleaned_description'].apply(cleaned2))
data.head(10)

"""**Model training**"""

from sklearn.model_selection import train_test_split
Independent_var =  data.cleaned_description_new
Dependent_var=data.Is_Response

IV_train,IV_test,DV_train,DV_test=train_test_split(Independent_var,Dependent_var,test_size=0.1,random_state=225)
print('IV_train :',len(IV_train))
print('IV_test :',len(IV_test))
print('DV_train :',len(DV_train))
print('DV_test :',len(DV_test))

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
tvec = TfidfVectorizer()
clf2 = LogisticRegression(solver="lbfgs")
from sklearn.pipeline import Pipeline

model=Pipeline([('vectorizer',tvec),('classifier',clf2)])
model.fit(IV_train,DV_train)

from sklearn.metrics import confusion_matrix
predictions=model.predict(IV_test)
confusion_matrix(predictions,DV_test)

"""**Model prediction**"""

from sklearn.metrics import accuracy_score,precision_score,recall_score

print("Accuracy :",accuracy_score(predictions,DV_test))
print("Precision :",precision_score(predictions,DV_test,average='weighted'))
print("Recall :",recall_score(predictions,DV_test,average='weighted'))

"""**Trying on new reviews**"""

example=["I'm  satisfied"]
result=model.predict(example)
print(result)