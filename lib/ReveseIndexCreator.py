#Inverted Index
from lib.TokenizeStemSWr import tokenizerWithFilter
import pandas as pd
import numpy as np


def creatInverseDict(localSave=True, dfInv=None,k = .01,titleExists = False):
    """
    It will create a dictionary of the reverse index
    
    if localSave = True, it will save it into the current directory
    """
    df = dfInv
    dict = {}
    if df is None:
        pd.read_pickle('data/tweetsTable.pickle')


    df['TF_IDF'] = 0.0
    df['TFIDF_Vector'] = 0.0
    
    R = df.shape[0]
    
    for index, document in df.iterrows():
        # create an array of tokens without stop words

        rawDocument = document['content']
        if 'title' in document:#determins weather we are looking at corpus or generating snippet
            rawDocument = rawDocument + (" " + document['title'])*3

        tokens_without_sw = tokenizerWithFilter(rawDocument)
        


        #df.at[index, 'Length'] = len(tokens_without_sw)
        #change one change this to 
        countOfMostCommentToken = mostCommonElementCount(tokens_without_sw)
        df.at[index,'mostCommonTokenCount'] = countOfMostCommentToken
        
        count = True
        # start appending if exits else create
        for item in tokens_without_sw:
            if not count:
                if item in dict:
                    if dict[item][0] != index:
                        dict[item].insert(0, index)
                # add word if not exits
                else:
                    dict[item] = []
                    dict[item].insert(0, index)
            else:
                # uncomment this for inverted index with counter on each document
                if item not in dict:
                    dict[item] = {}
                if index not in dict[item]:
                    dict[item][index] = 1
                elif index in dict[item]:
                    dict[item][index] += 1  # dict[item][index] + 1
        
        rTDIDF = np.empty(0)

        NT = len(tokens_without_sw)  
        
        qdf = pd.DataFrame(tokens_without_sw, columns=['Words'])
        qdf['Count'] = 1.0
        qdf = qdf.groupby('Words').count()
        
        for token, count in qdf.iterrows():
            NsT = count.Count
            RcD = len(dict[token])
            TF = (NsT/countOfMostCommentToken)*(1-k) + k
            IDF = (np.log2((1+R)/(1+RcD))+1)
            rTDIDF = np.append(rTDIDF, TF*IDF)
        df.at[index,'TFIDF_Vector'] = np.sqrt((rTDIDF**2).sum())
            

    dict = pd.DataFrame(dict.items(),columns=['index','token']).set_index(['index'],drop=True)          
    
    if localSave:
        dict.to_pickle('data/inverseIndexTable.pickle')
    else:
        return dict

from collections import Counter
def mostCommonElementCount(tokenList):
    """
    Returns the count of the most common element

    Example:
        myList = ['hello','hi','hi','mostCommon']

        mostCommonElementCount(myList)
        >>>> 2
    """
    if len(tokenList) == 0:
        return 1
    data = Counter(tokenList)
    return data[max(tokenList, key=data.get)]
