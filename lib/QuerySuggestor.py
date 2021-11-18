import pandas as pd
import getpass
from datetime import datetime
import os.path


def query_suggestor():
    """
    The purpose is to 
    """
    """pickle: data frame stored as a file.
    QueryLog.pickle contains list of queries from other users
    We will use this to make suggestions to the user for other
    queries they can make"""

    df = pd.read_pickle('data/QuerryLog.pickle')
    print('Please Enter a query below... Press enter after a space for suggestions')

    """initialize the whole query to an empty string.  This will become
    the user input, and possibly additional inputs as needed.  user_query
    is the user input for only a single iteration of the loop"""
    current_query = input()
    make_query_suggestions = current_query[-1] == " "
    while make_query_suggestions:
        # Query: name of column, np array string of queries
        # str: allows us to perform string operations on each row of the dataframe (df)
        # startswith: SQL-like command - "String% ..."
        string_start = current_query.strip().lower() + ' '  # add space at end to avoid suggesting original query
        suggestion_filter = df.Query.str.startswith(string_start, na=False)  # na=False: set NaN values to False to avoid errors

        # get all suggestions similar to query, but can have duplicates if they came from different users
        suggestions_unique_by_session = df[suggestion_filter].groupby(['Query', 'AnonID']).count()
        # num_of_sessions: number of queries that start with user input
        num_of_sessions = suggestions_unique_by_session.groupby(['AnonID']).count().shape[0]

        # get all suggestions, but only those that are completely unique
        suggestions_unique = suggestions_unique_by_session.groupby(['Query']).count().sort_values(['Score'], ascending=False).head(5)

        i = 0
        rows = suggestions_unique.shape[0]
        while i < rows:
            print("Score: " + str(round(suggestions_unique['Score'].values[i]/num_of_sessions, 3)) + '\tQuery: ' + str(suggestions_unique.index.values[i]))
            i += 1

        # now, start updating the query based on new/additional user input
        user_query = input(current_query)
        if len(user_query) == 0 or user_query[-1] != " ":
            make_query_suggestions = False
        else:
            # .strip() -> remove blank characters from start/end of string
            # cleans up input
            current_query = current_query.strip() + " " + user_query.strip()

    # update data/QueryLog.pickle with the user's final query only
    new_row = {
                'AnonID': getpass.getuser(),
                'Query': str(current_query.strip()),
                'QueryTime': str(datetime.now()),
                'Used': 0,
                'Appeared': 0,
                'Score': 0
            }
    df = df.append(new_row, ignore_index=True)
    df.to_pickle('data/QueryLog.pickle')

    return current_query.strip()
