import environ
from utils import get_db_handle, get_db_handle_connection_string
from pymongo.bson.objectid import ObjectId

env = environ.Env()

environ.Env.read_env()

def getDb():

    if env('DB_CONNECTION_TYPE') == 'CONNECTION_STRING':
        return get_db_handle_connection_string(env('DB_NAME'), env('DB_CONNECTION_STRING'))
    
        
    host = env(env('DB_NAME')+'_DB_HOST')
    port = env(env('DB_NAME') + '_DB_PORT')
    # username = env('DB_USERNAME')
    # password = env('DB_PASSWORD')
    return get_db_handle(env('DB_NAME'), host, port)

def serializeDbResults(queryResults):
    """
    finds all instances of ObjectId in queryResults dict and converts them to strings
    """
    if type(queryResults) == str or type(queryResults) == int or type(queryResults) == float or isinstance(queryResults, ObjectId):
        return str(queryResults) # if it's a string, int, or float, return it as a string
    elif type(queryResults) == dict:

        for key in queryResults:
            if isinstance(queryResults[key], dict) or isinstance(queryResults[key], list):
                queryResults[key] = serializeDbResults(queryResults[key])

    elif type(queryResults) == list:
        for i in range(len(queryResults)):
            queryResults[i] = serializeDbResults(queryResults[i])


def dbCallWrapper(*args, **kwargs):
    """
    requires:
        dbfunc = the db function you want to call
        eventLog = Bool (whether or not this db call should be logged)
        *args = the args you want to pass into the database function
    """
    eventLog = kwargs['eventLog'] or False 
    dbfunc = kwargs['func']

    queryResults = dbfunc(*args)

    if queryResults:
        return serializeDbResults(queryResults)
    else:
        raise Exception('Error: No results returned from database')
