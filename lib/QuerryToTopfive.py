import numpy as np
import pandas as pd
import math
from lib.TokenizeStemSWr import tokenizerWithFilter
from lib.ReveseIndexCreator import creatInverseDict


def retrieveTop5WithCosineTFIDF(query, inverseIndexDict=None, corpusDf=None, forceCreateReverseIndex=False):
    """
    Calculating TD-IDF is calculating the importance of a word compared to a resource
    
    query:
        A query of keywords your looking for inside documents

    inverseIndexDict:
        the inverse index of the corpus

        default = None : just take the inverse dictionary of the entire corpus located inside data/inverseIndexTable.npy

    corpusDf:
        a dataframe containing
            docID, content(text), Length(number of tokens), TDIDF_Vector (precomputed TFIDF between all the words in the
            document and the document), TD_DF (Cosine rank of the TD-IDF)

    forceCreateReverseIndex:
         if no inverseIndexDict is found it will attempt to locate it in data/inverseIndexTable.npy. The only exception
         to this is if this is set true, in which it will create an inverse index from the corpusDf
        
    """
    if corpusDf is None:
        corpusDf = pd.read_pickle('data/tweetsTable.pickle')

    if inverseIndexDict is None:
        if not forceCreateReverseIndex:
            try:
                inverseIndexDict = pd.read_pickle('data/inverseIndexTable.pickle')
            except:
                print('Unable To find inverse Index... We will create one, This will take an hour..., '
                      'email enochlev@gmail.com for the file and put it inside your data folder')
                input('Press Enter to Continue')
                creatInverseDict()
                inverseIndexDict = pd.read_pickle('data/inverseIndexTable.pickle')
                print('Done creating reverse index')
        else:
            # this is needed if we are trying to find cosine similarity of sentences inside a single article
            inverseIndexDict = creatInverseDict(localSave=False, dfInv=corpusDf)

    # necessary values of calcualting TD-IDF of query

    resource_count = corpusDf.shape[0]

    #This commented code should create a list of documents that contain any of the words in the query
    
    queryTokens = tokenizerWithFilter(query)
    
    listDoc=[]

    for item in queryTokens:
        if item in inverseIndexDict.index:
            for doc in inverseIndexDict[item:item].values[0][0]:
                if (doc -1) in listDoc:
                    pass
                else:
                    listDoc.append(doc-1)
    
    corpusDf = corpusDf.iloc[listDoc]

    # tokenize the query
    

    # obtain a count of unique tokens
    #
    # Example
    # if
    # queryTokens =
    # ['like','frozen','frozen','favorite','movie']
    #
    # then qdf will look something like this
    # word   |   count
    # like   |   1
    # frozen |   2
    # favorite|  1
    query_df = pd.DataFrame(queryTokens, columns=['Words'])
    query_df['Count'] = 1.0
    query_df = query_df.groupby('Words').count()

    """
    First attempt at smoothing (p1)
    Equation for IDF smoothing: Pera's notes, "What is (web) search?", pp. 64
    
    """
    # obtain number of tokens in the query
    # this is necessary for computing TD-IDF
    #mostCommon
    qLen = len(queryTokens)
    cosineRanks = []
    for resourceID, document in corpusDf[['mostCommonTokenCount','TFIDF_Vector']].iterrows():
        mostCommonTokenCount = document.mostCommonTokenCount
        #doc_count = document.Length

        # document is empty
        if mostCommonTokenCount == 0:
            cosineRanks.append(0)
        else:
            # make word to query TFIDF and word to resources TFIDF vectors
            doc_TFIDF = np.empty(0)
            query_TFIDF = np.empty(0)
            for qToken, queryFreq in query_df.iterrows():
                if qToken in inverseIndexDict.index:
                    query_TFIDF = np.append(query_TFIDF, queryFreq.Count / qLen)
                    doc_TFIDF = __compute_doc_tfidf(doc_TFIDF,
                                                    inverseIndexDict,
                                                    qToken,
                                                    resourceID,
                                                    mostCommonTokenCount,
                                                    resource_count)

            # ::::::::::::::::Cosine TF-IDF::::::::::::::::::::::#
            # Pera's notes: "What is (web) search?" pp. 61
            # tfidf_resource_vector_length (document.TDIDF_Vector) is pre-computed to save time
            tfidf_sums = (doc_TFIDF * query_TFIDF).sum()
            tfidf_query_vector_length = (np.sqrt((query_TFIDF**2).sum()))
            cosineRanks.append(tfidf_sums / (tfidf_query_vector_length * document.TFIDF_Vector))
    # saved into TD_IDF
    corpusDf['cosineTFIDF'] = cosineRanks

    five_sorted_values = corpusDf.sort_values('cosineTFIDF', ascending=False).head(5)
    tweetID = five_sorted_values.index.values
    Tweets = five_sorted_values.content.values

    if 'title' in corpusDf:
        rank = five_sorted_values['cosineTFIDF'].values
        i = 0
        while i < len(rank):
            if rank[i] is np.nan:
                rank[i] = 0
            i = i + 1
        title = five_sorted_values['title'].values
        return (tweetID, title, Tweets, rank)
    else:
        return (tweetID, Tweets)


def __compute_doc_tfidf(doc_tfidf, inverse_index_dict, query_token, resourceID, mostCommonTokenCount, resource_count,k =.01):
    dictList = inverse_index_dict[query_token:query_token].values[0][0]
    docs_with_token = len(dictList)
    curr_token_count = 0  # number of times the current token was seen in the current document
    if resourceID in dictList:
        curr_token_count = dictList[resourceID]
    # print(((curr_token_count/NT) * (np.log2((1+resource_count)/(1+docs_with_token))+1)))
    doc_TF = (curr_token_count / mostCommonTokenCount) * (1-k) + k
    doc_IDF = np.log2((1 + resource_count) / (docs_with_token + 1)) + 1  # with smoothing
    return np.append(doc_tfidf, doc_TF * doc_IDF)
