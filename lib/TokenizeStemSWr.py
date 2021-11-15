from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer

ps = PorterStemmer()
tokenizer = RegexpTokenizer(r'\w+')
stop_words = {}
try:
    stop_words = set(stopwords.words('english'))
except:
    print('StopWords not found... downloading <WordNet> and <StopWords>')
    import nltk
    nltk.download('wordnet')
    nltk.download('stopwords')
    print('Done Preceding')
    stop_words = set(stopwords.words('english'))


def tokenizerWithFilter(newText):
    """
    This Function will tokenize and apply filters to an entire sentence
    return a list of words
    """
    # split words and remove punctuation
    tokens = tokenizer.tokenize(newText)
    filtered_sentence = []
    for w in tokens:
        # remove stop words
        if w in stop_words:
            continue

        # remove numbers
        if w.isnumeric():
            continue

        # if the word is not a stop word, and not a number, and the characters are all ascii, then add the lowercase,
        # stemmed word to the return value
        if is_ascii(w):
            w = w.lower()
            w = ps.stem(w)
            filtered_sentence.append(w)
    return filtered_sentence


def is_ascii(s):
    return all(ord(c) < 128 for c in s)
