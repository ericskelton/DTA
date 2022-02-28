from api.utils.db import getDb, dbCallWrapper
from api.utils.errors import handleViewError
from datetime import datetime
from os import path
import time
import environ

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
        # Get the username
        # user = request.user.username
        user = "621c2225545c6aa5b6b9b83a" if env('HARD_CODED_USER') else request.user.id	
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
        }	
        json.update(request.GET.dict())
        json.update(request.POST.dict())		
        request.transactionId = dbCallWrapper(json, func = db.log.insert_one)
        
        
        return view(request, **kwargs)
        
    return wrapper

