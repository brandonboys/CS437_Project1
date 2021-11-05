import sys
import warnings
from lib.QuerryToTopfive import COSINE_TD_IDF_Ranking
from lib.SnippetGenerator import snippetGenerator
from lib.QuerySuggestor import query_suggestor
from lib.QueryLogger import logger
from os.path import exists
from google_drive_downloader import GoogleDriveDownloader as gdd
import pandas as pd
from datetime import datetime


if __name__ == "__main__":
    start_time = datetime.now()

    warnings.filterwarnings('ignore')

    # ask for a suggestion and return what the user wanted
    query = query_suggestor()

    # get top 5 results
    out = COSINE_TD_IDF_Ranking(query)

    i = 0
    while i < len(out[0]):
        # print out title
        print('Doc ID' + str(out[0][i]))
        print(str(round(float(out[3][i]), 3)*100) + "% Similarity")
        print(str(out[1][i]))

        # snip it
        # and display
        print(snippetGenerator(query, out[2][i]))
        print('\n')
        i += 1

    # log it
    logger(query)

    print(datetime.now() - start_time)
