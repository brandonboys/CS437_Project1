import sys
import warnings
from lib.QuerryToTopfive import COSINE_TD_IDF_Ranking 
from lib.SnippetGenerator import snippetGenerator
from lib.synonymSuggestor import querrySuggestor
from lib.QueryLogger import logger
from os.path import exists
from google_drive_downloader import GoogleDriveDownloader as gdd
import pandas as pd




#check if reverse index is decompressed
if exists('data/inverseIndexTable.npy') == False:
    print('Downloading the Inverse Index... Please Wait. Estimated Size 260-780 MB depending if google compresses it')
    gdd.download_file_from_google_drive(file_id='1daXFpn7lS2LTX59Xrdb9nkt4K2jx5pCb',
                                    dest_path='data/inverseIndexTable.npy',
                                    unzip=True)

if exists('data/tweetsTable.pickle') == False:
    if exists('data/tweetsTable.zip') == False:
        print('Downloading the Documents... Please Wait. Estimated Size 500 MB depending if google compresses it')
        gdd.download_file_from_google_drive(file_id='1vccCcUhlv08Pe8fisBfAcIDYyJ7I_r9V',
                                        dest_path='data/tweetsTable.zip',
                                        unzip=False)
    pd.read_pickle('data/tweetsTable.zip').to_pickle('data/tweetsTable.pickle')


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
    print(snippetGenerator(query,out[1][i]))
    print('\n')
    i+=1

##log it
logger(query)