#Inverted Index
from TokenizeStemSWr import tokenizerWithFilter
import pandas as pd


def creatInverseDict(localSave=True):
    """
    It will create a dictionary of the reverse index
    
    if localSave = True, it will save it into the current directory
    """
    dict = {}
    df = pd.read_pickle('tweetsTable.pickle')
    
    for index, tweet in df.iterrows():

        #create an array of tokens withot stop words
        tokens_without_sw = tokenizerWithFilter(tweet['tweets'])
        
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
        #input(tokenizerWithFilter(tweet))
    if localSave:
        np.save('inverseIndexTable.npy', dict) 
    else:
        return dict