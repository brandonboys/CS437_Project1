import numpy as np
import pandas as pd
import math
from lib.TokenizeStemSWr import tokenizerWithFilter
from lib.ReveseIndexCreator import creatInverseDict


def retreiveTop5WithCosineTDIDF(query, inverseIndexDict=None, corpusDf=None, forceCreateReverseIndex=False):
    """
    Calculating TD-IDF is calculating the importantce of a word compared to a recource    
    
    query:
        A query of keywords your looking for inside documents

    inverseIndexDict:
        the inverse index of the corpus

        default = None : just take the inverse dictionary of the entire corpus located inside data/inverseIndexTable.npy

    corpusDf:
        a dataframe containing
            docID, content(text), Length(number of tokens), TDIDF_Vector (precomputed TDIDF between all the words in the document 
            and the document),TD_DF (Cosine rank of the TD-IDF)

    forceCreateReverseIndex:
         if no inverseIndexDict is found it will attempt to located it in data/inverseIndexTable.npy. The only exception 
         to this is if this is set true, in which it will create an inverse index from the courpusDF 
        
    """
    if corpusDf is None:
        corpusDf = pd.read_pickle('data/tweetsTable.pickle')

    if inverseIndexDict is None:
        if not forceCreateReverseIndex:
            try:
                inverseIndexDict = np.load('data/inverseIndexTable.npy', allow_pickle='TRUE').item()
            except:
                print('Unable To find inverse Index... We will create one, This will take an hour..., '
                      'email enochlev@gmail.com for the file and put it inside your data folder')
                input('Press Enter to Continue')
                creatInverseDict()
                inverseIndexDict = np.load('data/inverseIndexTable.npy', allow_pickle='TRUE').item()
                print('Done creating reverse index')
        else:
            # this is needed if we are trying to find cosinesmilarity of sentances inside a single article
            inverseIndexDict = creatInverseDict(localSave=False, dfInv=corpusDf)

    # necessary values of calcualting TD-IDF of qerry

    R = corpusDf.shape[0]
    

    # This commented code should create a list of documents that contain any of the words in the query
    # listDoc=[]
    # for item in tokenizerWithFilter(query):
    #     if item in dict_inverse_index:
    #         for doc in dict_inverse_index[item]:
    #
    #             if (doc -1) in listDoc:
    #                 pass
    #             else:
    #                 listDoc.append(doc-1)
    #
    # df = df.iloc[listDoc]

    #tokenize the query
    queryTokens = tokenizerWithFilter(query)

    #optain number of tokens in the query
    #this is necessary for computing TD-IDF
    qLen = len(queryTokens)
    
    
    #obtain a count of unique tokens
    #
    #Example
    #if
    #queryTokens =
    #['like','frozen','frozen','favorite','movie']
    #
    #thenqdf will look somthing like this
    #word   |   count
    #like   |   1
    #frozen |   2
    #favorite|  1
    qdf = pd.DataFrame(queryTokens, columns=['Words'])
    qdf['Count'] = 1.0
    qdf = qdf.groupby('Words').count()

    #keep track of Cosine Rank between query and every document
    #:::::::::::::::::::TD-IDF with smoothing:::::::::::::::::#
    # NST: number specific word in document
    # NT: number of words in document
    # R: Number of Recources in the corups
    # RcD: Number of number of documents contained a specific word
    #
    # Note that R/RCD is always 1 when computer TD-IDF between a word in a query and the entire query
    #
    #    NST         / log2(1+R)    \
    #   -----   X   (-----------  + 1)
    #     NT         \ 1 + RcD      /
    cosineRanks = []
    for resourceID, tweet in corpusDf.iterrows():
        NT = tweet.Length

        #document is empty
        if NT == 0:
            cosineRanks.append(np.NaN)
            continue
        else:

            #make word to query TDIDF and word to recouces TDIDF vectors
            rTDIDF = np.empty(0)
            qTDIDF = np.empty(0)
            for qToken, queryFreq in qdf.iterrows():
                if qToken in inverseIndexDict:
                    qTDIDF = np.append(qTDIDF,queryFreq.Count / qLen)
        
                    RcD = len(inverseIndexDict[qToken])
                    
                    NsT = 0
                    if resourceID in inverseIndexDict[qToken]:
                        NsT = inverseIndexDict[qToken][resourceID]
                    # print(((NsT/NT) * (np.log2((1+R)/(1+RcD))+1)))

                    rTDIDF = np.append(rTDIDF,((NsT/NT) * (np.log2((1+R)/(1+RcD))+1)))
            

            #::::::::::::::::Cosine TD-IDF::::::::::::::::::::::#
            #rTDIDF: vector of TD-IDF between every word and the query
            #qTDIDF: vector between every word and the document
            #
            #             rTDIDF x qTDIDF
            # ---------------------------------------
            #  -/(SUM(qTDIDF^2)) * -/(SUM(rTDIDF^2))
            #
            #  note that -/(SUM(rTDIDF^2)) is precomputed and is sotred inside tweetsTable.pickl
            #            #
            cosineRanks.append(((rTDIDF * qTDIDF).sum()) / ((np.sqrt((qTDIDF**2).sum())) * tweet.TDIDF_Vector))


    #saved into TD_IDF
    corpusDf['cosineTDIDF'] = cosineRanks

    five_sorted_values = corpusDf.sort_values('cosineTDIDF', ascending=False).head(5)
    tweetID = five_sorted_values.index.values
    Tweets = five_sorted_values.content.values

    if 'title' in corpusDf:
        rank = five_sorted_values['cosineTDIDF'].values
        i = 0
        while i < len(rank):
            if rank[i] is np.nan:
                rank[i] = 0
            i = i + 1
        title = five_sorted_values['title'].values
        return (tweetID, title, Tweets, rank)
    else:
        return (tweetID, Tweets)