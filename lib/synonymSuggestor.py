import pandas as pd
import getpass
from datetime import datetime



def querrySuggestor():
    """
    The purpose is to 
    """
    df =pd.read_pickle('data/QuerryLog.pickle')
    print('Please Enter a query below... Press enter after a space for suggestions')
    ln = ' '
    first = True
    while ln[len(ln)-1] == " ":
        newinput = input(ln)
        if newinput == "":
            break
        ln = ln.strip() + " " + newinput
        
        i = 0
        
        if ln[len(ln)-1] != " ":
            break
        
        sug = df[df.Query.str.startswith((ln.strip().lower() + ' '),na=False)].groupby(['Query','AnonID']).count()
        numOfSessions = sug.groupby(['AnonID']).count().shape[0]
        sug = sug.groupby(['Query']).count().sort_values(['Score'],ascending=False).head(5)
        
        i = 0
        while i < sug.shape[0]:
            print("Score: " + str(round(sug['Score'].values[i]/numOfSessions,3)) + '   Query: '  + str(sug.index.values[i]))
            i+=1
        first = False
    

    newRow = {'AnonID':getpass.getuser(),'Query':str(ln.strip()),'QueryTime':str(datetime.now()),'Used':0,'Appeared':0,'Score':0}
    df =df.append(newRow,ignore_index=True)
    df.to_pickle('data/QuerryLog.pickle')
    return (ln.strip())
