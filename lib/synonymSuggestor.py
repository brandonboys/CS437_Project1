import pandas as pd
df =pd.read_pickle('data/QuerryLog.pickle')


def querrySuggestor():
    """
    The purpose is to 
    """
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

            return (ln.strip())
        
        sug = df[df.Query.str.startswith((ln.strip().lower() + ' '),na=False)].groupby(['Query','AnonID']).count()
        numOfSessions = sug.groupby(['AnonID']).count().shape[0]
        sug = sug.groupby(['Query']).count().sort_values(['Score'],ascending=False).head(5)
        
        i = 0
        while i < sug.shape[0]:
            print("Score: " + str(round(sug['Score'].values[i]/numOfSessions,3)) + '   Query: '  + str(sug.index.values[i]))
            i+=1
        first = False
    
    return (ln.strip())
