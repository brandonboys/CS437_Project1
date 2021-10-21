import pandas as pd
from lib.QuerryToTopfive import COSINE_TD_IDF_Ranking


def snippetGenerator(originalQuery, sentance):
    """
    The goal is to compute the most similar setentces to each query to create a snippet that consists of two sentances.
    Use TD-IDF if you can

    Example Input:
    originalQuery="Russia China"
    sentance="Trump Loves Russia. Biden took bribe from China. I hate politics."
    Example Output:
    "Trump Loves Russia. Biden took bribe from China.
    """
    sentances = split_into_sentences(sentance)
    indexes = list(range(len(sentances)))

    dfDoc = pd.DataFrame(sentances,columns=['content'])
    dfDoc.index += 1

    out = COSINE_TD_IDF_Ranking(originalQuery, dict_inverse_index=None, df=dfDoc, forceCreateRevIndex=True)

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