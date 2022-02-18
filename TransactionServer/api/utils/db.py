import environ
from utils import get_db_handle, get_db_handle_connection_string

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

