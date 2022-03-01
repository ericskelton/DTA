from rest_framework import status
from rest_framework.response import Response
import environ
import time
from api.utils.db import getDb, dbCallWrapper

# initialize the environment
env = environ.Env()
env.read_env()
db, client = getDb()

# moved from log to avoid circular import
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
    timestamp = int(time.time() * 1000)

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
def handleViewError(exception, request):
    """
    Handles a view error.
    """
    logError(exception, request)
    statuses = {
        'UserNotFound': status.HTTP_404_NOT_FOUND,
        'UserAlreadyExists': status.HTTP_409_CONFLICT,
        'InvalidRequest': status.HTTP_400_BAD_REQUEST,
        'InsufficientFunds': status.HTTP_400_BAD_REQUEST,
        'InvalidTicker': status.HTTP_400_BAD_REQUEST,
        'InvalidTransaction': status.HTTP_400_BAD_REQUEST,
        'InvalidTransactionType': status.HTTP_400_BAD_REQUEST,
        'InvalidTransactionStatus': status.HTTP_400_BAD_REQUEST,
        'NotEnoughFunds': status.HTTP_400_BAD_REQUEST,
        'InvalidUser': status.HTTP_400_BAD_REQUEST,
        'InvalidUserStatus': status.HTTP_400_BAD_REQUEST,
    }
    return Response(
        {'error': exception.args[0]},
        status= statuses[exception.args[0]] if exception.args[0] in statuses else status.HTTP_400_BAD_REQUEST
    )