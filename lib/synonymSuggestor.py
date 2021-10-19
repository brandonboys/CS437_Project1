import pandas as pd
df =pd.read_pickle('data/QuerryLog.pickle')


def querrySuggestor():
    """
    The purpose of this function is to change find synonyms of querry terms so that all tokens in the query are located in the reverse index

    Example Input:
    #let assume "extravagant" is not in the inverse index but "great" is
    query = Trumps extravagant policies are great
    Examples Ouput:
    query = Trump great policies are great
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
        
        while first == False and i < sug.shape[0]:
            if sug['Query'].values[i] == ln.strip().lower():
                df.at[sug.index[i],'Used'] += 1
            i+=1
        
        if ln[len(ln)-1] != " ":

            df.to_pickle('data/QuerryLog.pickle')
            return (ln.strip(),False)
        
        df['Score'] = df['Used']/df['Appeared']
        sug = df[df.Query.str.startswith((ln.strip().lower() + ' '),na=False)].sort_values(['Score'],ascending=False).head(5)
        i = 0
        while i < sug.shape[0]:
            df.at[sug.index[i],'Appeared'] +=1
            print("Score: " + str(round(sug['Score'].values[i],3)) + '   Query: '  + str(sug['Query'].values[i]))
            i+=1
        first = False
    
    df.to_pickle('data/QuerryLog.pickle')
    return (ln.strip(), True)
