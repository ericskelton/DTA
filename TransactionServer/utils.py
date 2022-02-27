from pymongo import MongoClient

def get_db_handle(db_name,host, port ):

    client = MongoClient(host=host,
                      port=int(port)
                     )
    db = client[db_name]
    return db, client

def get_db_handle_connection_string(db_name, connection_string):

    client = MongoClient(connection_string)
    db = client[db_name]
    return db, client