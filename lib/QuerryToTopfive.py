import numpy as np
import pandas as pd
from lib.TokenizeStemSWr import tokenizerWithFilter
from lib.ReveseIndexCreator import creatInverseDict


def COSINE_TD_IDF_Ranking(query, dict_inverse_index=None, df=None, forceCreateRevIndex=False):
    """
    Calculating TD-IDF is calculating the importantce of a word compared to a recource    
    Input Example:
    COSINE_TD_IDF_Ranking("I like Biden")
    #note df and dict should be inside the "data" folder
    
    OutPut: (format array with tuples)    
    [[1324365009359654914,'I meant if you bet the odds exactly (I.e"," if Biden has a 69% chance to win X then you bet 69 dollars on a Biden win and 31 dollars on a Biden loss). Place enough bets like that and you should break even"," or nearly so"," in a good model\n']
     [1324556160570171392,'Right. That\'s why I ask"," because we\'re more likely to see GA and its 16 electoral votes flip to Biden tonight rather than NV or PA. So I\'m curious if the Biden campaign is counting AZ in the win column or not"," because if they are"," GA in the Biden column would give him the win.\n']
     [1323973402294628354,"I'm not in the US and extremely anxious about Biden winning. It will be devastating. I dont think people realise how terrible a biden administration will be for US and world. Not liking trumps personality is not a good enough reason to vote for Biden. Gonna be a rough 4 years.\n"]
     [1323451721054564352,'I really like Pete Buttigieg. I do hope Biden pulls him into the team! He has been essential to Bidens campaign efforts and should serve in some capacity for his relentless efforts to put Biden back into the White House.#BidenHarris2020']
     [1323844576344449024,'I mean"," "I don\'t like Biden""," fine. "Biden isn\'t trustworthy","" fine. "Biden seems ugly?". Rude"," but fine. "Biden is a pinemarten." Problem. He is not a pinemarten. And nor is HE A FUCKING SOCIALIST.\n']]
        
    """
    if df is None:
        df = pd.read_pickle('data/tweetsTable.pickle')

    if dict_inverse_index is None:
        if not forceCreateRevIndex:
            try:
                dict_inverse_index = np.load('data/inverseIndexTable.npy', allow_pickle='TRUE').item()
            except:
                print('Unable To find inverse Index... We will create one, This will take an hour..., '
                      'email enochlev@gmail.com for the file and put it inside your data folder')
                input('Press Enter to Continue')
                creatInverseDict()
                dict_inverse_index = np.load('data/inverseIndexTable.npy', allow_pickle='TRUE').item()
                print('Done creating reverse index')
        else:
            # this is needed if we are trying to find cosinesmilarity of sentances inside a single article
            dict_inverse_index = creatInverseDict(localSave=False, dfInv=df)

    # necessary values of calcualting TD-IDF of qerry
    queryTokens = tokenizerWithFilter(query)
    qLen = len(queryTokens)
    qdf = pd.DataFrame(queryTokens, columns=['Words'])
    qdf['Count'] = 1.0
    qdf = qdf.groupby('Words').count()
    
    R = df.shape[0]
    cosineRanks = []
    
    for resourceID, tweet in df.iterrows():
        NT = tweet.Length
        if NT == 0:
            cosineRanks.append(np.NaN)
            continue
            
        rTDIDF = np.empty(0)
        qTDIDF = np.empty(0)
        for qToken, queryFreq in qdf.iterrows():
            if qToken in dict_inverse_index:
                qTDIDF = np.append(qTDIDF,queryFreq.Count / qLen)
                
                # OLD:RcD = len(dict[qToken])
                RcD = dict_inverse_index[qToken]['len']
                
                NsT = 0
                if resourceID in dict_inverse_index[qToken]:
                    NsT = dict_inverse_index[qToken][resourceID]
                    
                rTDIDF = np.append(rTDIDF, ((NsT/NT) * (R/RcD)))
                    
        cosineRanks.append((rTDIDF * qTDIDF).sum() /(np.sqrt((rTDIDF**2).sum()) * np.sqrt((qTDIDF**2).sum())))

    df.TD_IDF = cosineRanks
    five_sorted_values = df.sort_values('TD_IDF', ascending=False).head(5)
    tweetID = five_sorted_values.index.values
    Tweets = five_sorted_values.content.values

    if 'title' in df:
        title = five_sorted_values['title'].values
        return (tweetID, title, Tweets)
    else:
        return (tweetID, Tweets)



