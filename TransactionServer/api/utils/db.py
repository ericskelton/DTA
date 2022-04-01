import environ
from utils import get_db_handle, get_db_handle_connection_string
from bson.objectid import ObjectId
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult
from pymongo.cursor import Cursor

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
    if isinstance(queryResults, Cursor):
        return serializeDbResults(list(queryResults))
    if isinstance(queryResults, InsertOneResult) or isinstance(queryResults, UpdateResult):
        if queryResults.acknowledged:
            if isinstance(queryResults, UpdateResult) and queryResults.matched_count == 0:
                raise Exception('Error: No document with that _id was found')
            return str(queryResults.inserted_id) if isinstance(queryResults, InsertOneResult) else "Updated"
        raise Exception('Error: Database call failed')
    if type(queryResults) == str or type(queryResults) == int or type(queryResults) == float or isinstance(queryResults, ObjectId):
        return str(queryResults) # if it's a string, int, or float, return it as a string
    elif type(queryResults) == dict:

        for key in queryResults:
            if isinstance(queryResults[key], dict) or isinstance(queryResults[key], list):
                queryResults[key] = serializeDbResults(queryResults[key])
        
        return queryResults

    elif type(queryResults) == list:
        for i in range(len(queryResults)):
            queryResults[i] = serializeDbResults(queryResults[i])

        return queryResults

def logJsonObject(json):
    """
    Logs a json object.
    to the database log collection
    """
    if(not env('LOG')):
        return
    db, client = getDb()
    
    return dbCallWrapper(json, func = db.log.insert_one)
def dbCallWrapper(*args, **kwargs):
    """
    requires:
        dbfunc = the db function you want to call
        eventLog = Bool (whether or not this db call should be logged)
        *args = the args you want to pass into the database function
    """
    if 'eventLog' in kwargs.keys():
        eventLog = kwargs['eventLog']
    else:
        eventLog = False
    dbfunc = kwargs['func']
    if "except_on_not_found" in kwargs.keys():
        except_on_not_found = kwargs['except_on_not_found']
    else:
        except_on_not_found = False
    queryResults = dbfunc(*args)
    # print(queryResults)
    if isinstance(eventLog, dict):
        logJsonObject(eventLog)
    if queryResults:

        results = serializeDbResults(queryResults)
        return results
    elif except_on_not_found:
        raise Exception('Error: No results returned from database')
    else:
        return False

def mongoZip(fields):
    """
    takes a list of fields and zips them into a dict with field name as key and 1 as value
    """
    return dict(zip(fields, [1]*len(fields)))

