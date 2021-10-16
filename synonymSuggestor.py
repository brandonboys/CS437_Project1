from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
import pandas as pd
import math
import numpy as np
from nltk.corpus import wordnet



dict #Inverse Index: imported from a picke file



ps = PorterStemmer()
tokenizer = RegexpTokenizer(r'\w+')
stop_words = set(stopwords.words('english'))

def tokenizerWithFilter(newText):
    """
    This Function will tokenize and apply filters to an entire sentance... 
    return a list of words
    """
    ## split words and remove punctuation
    tokens = tokenizer.tokenize(newText)
    filtered_sentence = []
    for w in tokens:
        
        ## remove stop words
        if w not in stop_words:

            #to Lowercase
            w = w.lower()

            ##lemantize
            w = ps.stem(w)
            filtered_sentence.append(w)
    return filtered_sentence
    

#Check if every word exits in the dictionary
query = 'Hello This is an example Query'
filiteredQuery = tokenizerWithFilter(query)#['hello', 'thi', 'exampl', 'queri']



for word in filiteredQuery:
    if word in dict:
        #good
        pass
    else:
        synonyms = []



        #create an array of synonyms
        for syn in wordnet.synsets("active"):
            for l in syn.lemmas():
                synonyms.append(l.name())
                
        #check if any synonym exits in index
        for possibleWord in synonyms:
                     
            if tokenizerWithFilter(possibleWord)[0] in dict:
                print(True)
            else:
                print(False)
            #make qury suggestion

synonyms = []



#create an array of synonyms
for syn in wordnet.synsets("active"):
    for l in syn.lemmas():
        synonyms.append(l.name())


for possibleWord in synonyms:
    if tokenizerWithFilter(possibleWord)[0] in dict:
        print(True)
    else:
        print(False)