#Importing Librares
import pandas as pd
import numpy as np
import nltk
import re

nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer

df = int(input())

#ShortForm -> Stemming
ps = PorterStemmer()

#Text Pre-Processing
data = []
for i in range(0,1000):
    review = df[i]
    review = re.sub('[^a-zA-Z]',' ',review)
    review = review.lower()
    review = review.split()
    review = [ps.stem(w) for w in review if w not in set(stopwords.words('english'))]
    review = ' '.join(review)
    data.append(review)

#Convert Text into Array
cv = CountVectorizer()
x = cv.fit_transform(data).toarray()

#Y value for ANN
y = df.values

#ANN Model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

#ANN Block
model = Sequential()
model.add(Dense(1500,activation = 'relu'))
model.add(Dense(3000,activation = 'relu'))
model.add(Dense(1,activation='sigmoid'))

#Compiling
model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])

#Train the Model
model.fit(x,y,epochs=10)