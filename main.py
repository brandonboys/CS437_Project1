import sys
from QuerryToTopfive import COSINE_TD_IDF_Ranking 
import warnings
from FrenchFilter import frenchFilter
from SnippetGenerator import snippetGenerator
from synonymSuggestor import querrySuggestor
from QueryLogger import logger

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