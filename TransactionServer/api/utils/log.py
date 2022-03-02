from api.utils.db import getDb, dbCallWrapper
from api.utils.errors import handleViewError
from datetime import datetime
from os import path
import time
import environ
import pymongo

# initialize the environment
env = environ.Env()
env.read_env()





db, client = getDb()
def logRequest(view):
    """   
    Logs the command sent to the API.
    to the database log collection
    catches all exceptions and logs them
    """ 
    def wrapper(request, **kwargs):
        if(not env('LOG')):
            return view(request)
        timestamp = str(int(time.time()))	
        # get the last transactionNum from the database
        transactionNum = db.log.find_one({'type': 'userCommand'}, {'transactionNum': 1}, sort=[('_id', pymongo.DESCENDING)])
        
        transactionNum = transactionNum['transactionNum'] + 1 if 'transactionNum' in transactionNum.keys() else 1
        # Get the username
        # user = request.user.username
        user = "test" if env('HARD_CODED_USER') else request.user.id	
        # Get the command name
        command = request.path.split('/')[-2]	
        # Get the parameters	
        # Create the JSON
        json = {
        	'type': 'userCommand',
        	'timestamp': timestamp,
        	'userid': user,
        	'command': command,
        	'server': 'transactionserver',
            'transactionNum': transactionNum   
        }	
        json.update(request.GET.dict())
        json.update(request.POST.dict())
        dbCallWrapper(json, func = db.log.insert_one)
        request.transactionId = transactionNum
        
        
        return view(request, **kwargs)
        
    return wrapper

