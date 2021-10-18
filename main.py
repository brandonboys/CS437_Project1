import sys
import warnings
from lib.QuerryToTopfive import COSINE_TD_IDF_Ranking 
from lib.FrenchFilter import frenchFilter
from lib.SnippetGenerator import snippetGenerator
from lib.synonymSuggestor import querrySuggestor
from lib.QueryLogger import logger

warnings.filterwarnings('ignore')

query = ' '.join(sys.argv[1:])

#ask for a suggestion and return what the user wanted
query = querrySuggestor(query)


##get top 5 results
out = COSINE_TD_IDF_Ranking(query)

i = 0
while i < 5:
    #print out title
    print('Tweet ID' + str(out[0][i]))

    #snip it
    #french filter it
    #and display
    print(frenchFilter(snippetGenerator(query,out[1][i])))
    print('\n')
    i+=1

##log it
logger(query)