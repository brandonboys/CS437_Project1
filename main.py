import sys
from QuerryToTopfive import COSINE_TD_IDF_Ranking 
import warnings
from FrenchFilter import frenchFilter
from SnippetGenerator import snippetGenerator
from synonymSuggestor import querrySuggestor

warnings.filterwarnings('ignore')

query = ' '.join(sys.argv[1:])
query = querrySuggestor(query)



out = COSINE_TD_IDF_Ranking(query)

i = 0
while i < 5:
    print('Tweet ID' + str(out[0][i]))
    print(frenchFilter(snippetGenerator(query,out[1][i])))
    print('\n')
    i+=1
