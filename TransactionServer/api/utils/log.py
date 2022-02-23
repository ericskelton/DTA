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
    def wrapper(request):
        if(not env('LOG')):
            return view(request)
        timestamp = str(int(time.time()))	
        # Get the username
        # user = request.user.username
        user = "6211857dc98b9aa98bf047a9" if env('HARD_CODED_USER') else request.user.id	
        # Get the command name
        command = request.path.split('/')[-1]	
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
        try:
            return view(request)
        except Exception as e:
            return handleViewError(e, request)
    return wrapper	



def logError(exception, request):
    """
    Logs an error.
    to the file BASE_DIR/logs/transactionserver.xml
    XML format:
    <errorEvent>
      <timestamp><current unix timestamp/></timestamp>
      <server>Transaction Server</server>
      <errorMessage><error message/></errorMessage>
      <command><command name/></command>
      <parameters><parameters/></parameters>
      <transactionNum><transactionNum/></transactionNum>
    </errorEvent>

    """

    if(not env('LOG')):
        return

    # Get the current timestamp
    timestamp = str(int(time.time()))

    # Get the error message
    errorMessage = exception.args[0]

    # Get the command name
    command = request.path.split('/')[-1]

    # Get the parameters
    json = {
        'type': 'errorEvent',
        'timestamp': timestamp,
        'server': 'transactionserver',
        'errorMessage': errorMessage,
        'command': command,
        'transactionId': request.transactionId
    }
    json.update(request.GET.dict())
    json.update(request.POST.dict())

    
    dbCallWrapper(json, func = db.log.insert_one)
    
    return 

def logJson(json):
    """
    Logs a json object.
    to the database log collection
    """
    if(not env('LOG')):
        return
    dbCallWrapper(json, func = db.log.insert_one)
    return