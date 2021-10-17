from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer

ps = PorterStemmer()
tokenizer = RegexpTokenizer(r'\w+')
stop_words = {}
try:
    stop_words = set(stopwords.words('english'))
except:
    print('StopWords not found... please download <WordNet> and <StopWords>\nBoth located under corpora')
    import nltk
    nltk.download()


def tokenizerWithFilter(newText):
    """
    This Function will tokenize and apply filters to an entire sentance... 
    return a list of words
    """
    ## split words and remove punctuation
    tokens = tokenizer.tokenize(newText)
    filtered_sentence = []
    for w in tokens:
        
        ## remove stop words
        if w not in stop_words and (False == w.isnumeric()):

            #to Lowercase
            w = w.lower()

            ##lemantize
            w = ps.stem(w)
            filtered_sentence.append(w)
    return filtered_sentence