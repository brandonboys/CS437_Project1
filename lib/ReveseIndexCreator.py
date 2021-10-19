#Inverted Index
from lib.TokenizeStemSWr import tokenizerWithFilter
import pandas as pd


def creatInverseDict(localSave=True,dfInv=None):
    """
    It will create a dictionary of the reverse index
    
    if localSave = True, it will save it into the current directory
    """
    df = dfInv
    dict = {}
    if df == None:
        pd.read_pickle('data/tweetsTable.pickle')

    df['Tokens'] = object
    df['Length'] = 0
    df['TD_IDF'] = 0.0

    
    for index, tweet in df.iterrows():

        #create an array of tokens withot stop words
        tokens_without_sw = tokenizerWithFilter(tweet['content'])
        
        df.at[index,'Tokens'] = tokens_without_sw
        df.at[index,'Length'] = len(tokens_without_sw)
        count = True
        
        #start appending if exits else create
        for item in tokens_without_sw:
            if False==count:
                #add word if not exits
                if item not in dict:
                    dict[item] = []
                    dict[item].insert(0,index)

                if item in dict:
                    if dict[item][0] != index:
                        dict[item].insert(0,index)

            else:
                #uncomment this for inverted index with counter on each document
                if item not in dict:
                    dict[item] = {}
                if index not in dict[item]:
                    dict[item][index] = 1
                elif index in dict[item]:
                    dict[item][index] += 1#dict[item][index] + 1
    for word in dict:
        dict[word]['len'] = len(dict[word])
        
    if localSave:
        np.save('data/inverseIndexTable.npy', dict) 
    else:
        return dict