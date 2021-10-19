import getpass
from datetime import datetime

def logger(query):
    """
    the purpose here is to add on the querylog.txt to access a history of logs
    You will need to check the homework on the details a log needs to cotain
    """



    log = '\n' + str(getpass.getuser()) + "\t" + str(query) + "\t" + str(datetime.now()) 


    # Open a file with access mode 'a'
    file_object = open('log.txt', 'a')
    # Append 'hello' at the end of file
    file_object.write(log)
    # Close the file
    file_object.close()
