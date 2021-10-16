import sys
from QuerryToTopfive import COSINE_TD_IDF_Ranking 
import warnings
warnings.filterwarnings('ignore')

query = ' '.join(sys.argv[1:])


out = COSINE_TD_IDF_Ranking(query)

i = 0
while i < 5:
    print(out[1][i])
    print('\n')
    i+=1
