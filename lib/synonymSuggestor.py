from lib.TokenizeStemSWr import tokenizerWithFilter
from nltk.corpus import wordnet
import numpy as np
dict = np.load('data/inverseIndexTable.npy',allow_pickle='TRUE').item()

def querrySuggestor(query):
    """
    The purpose of this function is to change find synonyms of querry terms so that all tokens in the query are located in the reverse index

    Example Input:
    #let assume "extravagant" is not in the inverse index but "great" is
    query = Trumps extravagant policies are great
    Examples Ouput:
    query = Trump great policies are great
    """

    #Check if every word exits in the dictionary
    filiteredQuery = tokenizerWithFilter(query)#['hello', 'thi', 'exampl', 'queri']
    querrySuggestions = []
    querrySuggestions.append(query)

    for word in query.split():
        if len(tokenizerWithFilter(word)) == 0 or (tokenizerWithFilter(word)[0] in dict):
            #good
            pass
        else:
            #find synoyms
            synonyms = []

            #create an array of synonyms
            for syn in wordnet.synsets(word):
                for l in syn.lemmas():
                    synonyms.append(l.name())
                    
            if len(synonyms) == 0:
                #no suggestions exist
                continue #on to next word
            #check if any synonym exits in index
            for possibleWord in synonyms:                        
                if tokenizerWithFilter(possibleWord)[0] in dict:
                    querrySuggestions.append(query.replace(word,possibleWord,1))
                    break# looking for synonyms and go to the nextword
                    
    if len(querrySuggestions) > 1:
        i =1
        print("\nplease select a suggested querry")
        for pquery in querrySuggestions:
            print(str(i) + ") " + pquery)
            i+=1
        qnum = "notNum"
        qnum = input()
        i = 3
        while qnum.isnumeric() == False or (int(qnum) <=0 or int(qnum) >= i):
            qnum = input("invalid\n")

        return querrySuggestions[int(qnum)-1]
        
    return query
