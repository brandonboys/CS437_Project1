import getpass
from datetime import datetime

import pandas as pd
df =pd.read_pickle('data/QuerryLog.pickle')


def logger(query):
    """
    the purpose here is to add on the querylog.txt to access a history of logs
    You will need to check the homework on the details a log needs to cotain
    """
    df =pd.read_pickle('data/QuerryLog.pickle')
    df.append([{'AnonID':str(getpass.getuser()),'Query':str(query),'QueryTime':str(datetime.now()),'Score':0,'Appeared':0,'Used':0}],ignore_index=True)
    df.to_pickle('data/QuerryLog.pickle')

