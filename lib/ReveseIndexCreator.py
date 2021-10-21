#Inverted Index
from lib.TokenizeStemSWr import tokenizerWithFilter
import pandas as pd
import numpy as np


def creatInverseDict(localSave=True, dfInv=None):
    """
    It will create a dictionary of the reverse index
    
    if localSave = True, it will save it into the current directory
    """
    df = dfInv
    dict = {}
    if df is None:
        pd.read_pickle('data/tweetsTable.pickle')

    df['Length'] = 0
    df['TD_IDF'] = 0.0
    df['TDIDF_Vector'] = 0.0
    
    R = df.shape[0]
    
    for index, tweet in df.iterrows():
        # create an array of tokens without stop words
        tokens_without_sw = tokenizerWithFilter(tweet['content'])
        
        df.at[index, 'Length'] = len(tokens_without_sw)
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
            rTDIDF = np.append(rTDIDF, ((NsT/NT) * (np.log2((1+R)/(1+RcD))+1)))
        df.at[index,'TDIDF_Vector'] = np.sqrt((rTDIDF**2).sum())
            

              
        
    if localSave:
        np.save('data/inverseIndexTable.npy', dict) 
    else:
        return dict
