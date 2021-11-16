import pandas as pd
from lib.QuerryToTopfive import retrieveTop5WithCosineTFIDF


def snippetGenerator(originalQuery, sentance):
    """
    The goal is to compute the most similar setentces to each query to create a snippet that consists of two sentances.
    Use TD-IDF if you can
    """
    sentances = split_into_sentences(sentance)

    #create a dataFrame with the document devided into rows of the table
    dfDoc = pd.DataFrame(sentances,columns=['content'])
    #Make index start with 1 and not 0
    dfDoc.index += 1

    #pass in dfDoc as corpus and force create inverse dictionary
    out = retrieveTop5WithCosineTFIDF(originalQuery, inverseIndexDict=None, corpusDf=dfDoc, forceCreateReverseIndex=True)

    # print out top two sentances as snippet
    if(len(out[1]) == 0 or len(out[1]) == 1):
        return sentance
    return str(out[1][0]) + " " + str(out[1][1])



import re
def split_into_sentences(text):
    alphabets= "([A-Za-z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov)"
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences