
from api.utils.db import getDb
import time
from api.utils.quoteServer import getQuote
from hashlib import sha256
from bson.objectid import ObjectId
from api.utils.db import dbCallWrapper

db, client = getDb()

def getBalance(oid):
    oid = ObjectId(oid)
    return dbCallWrapper({'_id': oid}, {'balance': 1}, func = db.user.find_one, eventLog = False)

def addBalance(oid, amount, transactionId):
    id = ObjectId(oid)
    print('amount', amount)
    return dbCallWrapper({"_id": id}, {'$inc': {'balance': float(amount)}}, func = db.user.update_one, eventLog = {'type': 'debugEvent', 'username': str(id), 'timestamp': int(time.time()), 'action': 'ADD_BALANCE', 'amount': amount, 'transactionId': transactionId})


def subBalance(id, amount):
    id = ObjectId(id)
    return dbCallWrapper({'_id': id}, {'$inc': {'balance': -float(amount)}}, func = db.user.update_one, eventLog = False) 

def getTransactions(id):
    id = ObjectId(id)
    return dbCallWrapper({'_id': id}, {'transactions': 1}, func = db.user.find_one, eventLog = False)

def getAllTransactions():
    return dbCallWrapper({}, {'transactions': 1}, func = db.user.find, eventLog = False)

def getUser(id):
    id = ObjectId(id)
    return dbCallWrapper({"_id": id}, func = db.user.find_one, eventLog = False)

def addTransaction(id, transaction):
    id = ObjectId(id)
    return dbCallWrapper({'_id': id}, {'$push': {'transactions': transaction}}, func = db.user.update_one)


def createUser(name, email, password):
    # email must be unique
    if(db.user.find_one({'email': email})): # don't need to wrap this 
        raise Exception('Email already in use')

    return dbCallWrapper({
        'name': name,
        'email': email,
        'password': sha256(password.encode('utf-8')).hexdigest(),
        'balance': 0.00, 
        'transactions': [], 
        'stocks': {},
        'pending_buy':{},
        'pending_sell':{},
        'sell_triggers': {},
        'buy_triggers': {},
        'pending_trigger': {}
        }, func = db.user.insert_one)

def login(email, password):
    user = dbCallWrapper({'email': email, 'password': sha256(password.encode('utf-8')).hexdigest()}, func = db.user.find_one)

    if(user):
        # TODO: generate token, return token
        return user
    else:
        return False

# sets the pending transaction to the pending transaction field on the user
# fails if the user does not have enough balance
def buyStock(id, amount, quote, transactionId):
    id = ObjectId(id)
    price = quote['price']
    stock = quote['ticker']
    timestamp = quote['timestamp']
    cryptographicKey = quote['cryptographicKey']
    user = getUser(id)
    # check if the user has enough balance to buy
    if(user['balance'] >= amount * price):

        # set pending transaction
        dbCallWrapper({'_id': id}, {
            '$set': {
                'pending_buy' : {
                    'stock': stock, 
                    'amount': amount, 
                    'price': price, 
                    'timestamp': timestamp, 
                    'cryptographicKey': cryptographicKey
                }
            }
        }, func = db.user.update_one, eventLog = {'type': 'debugEvent', 'username': str(id), timestamp: int(time.time()), 'action': 'BUY', 'stock': stock, 'amount': amount, 'price': price, 'cryptographicKey': cryptographicKey, 'transactionId': transactionId})
        return {
            'stock': stock,
            'amount': amount,
            'price': price,
            'timestamp': timestamp,
        }
    raise Exception('Insufficient balance')

# removes the pending buy
# adds the transaction to the transactions list
# if the any quote is over 1 minute old, we fail 
def commitBuy(id, transactionId):
    id = ObjectId(id)
    user = getUser(id)
    transaction = user['pending_buy']
    if(transaction):
        if(float(time.time()) - float(transaction['timestamp']) > 60):
            # clear the pending transaction
            db.user.update_one({'_id': id}, {'$set': {'pending_buy': None}})
            raise Exception('Quote expired')
        else:
            # buy the stock
            if(transaction['stock'] in user['stocks']):
                dbCallWrapper( {'_id': id}, {
                    '$inc': {
                        'stocks.' + transaction['stock'] + '.amount': transaction['amount'],
                        'balance': -transaction['amount'] * transaction['price']
                    }, 
                    '$push':{
                        'stocks.' + transaction['stock'] + '.price': {
                            str(transaction['amount']): transaction['price']
                        },
                        'transactions': transaction
                    },
                    '$set': {'pending_buy': None}
                }, func = db.user.update_one, eventLog = {'type': 'accountTransaction', 'username': str(id), 'timestamp': int(time.time()), 'action': 'BUY_SHARES', 'stock': transaction['stock'], 'amount': transaction['amount'], 'price': transaction['price'], 'cryptographicKey': transaction['cryptographicKey'], 'transactionId': transactionId})
                
            else:
                dbCallWrapper( {'_id': id}, {
                    '$set': {
                        'stocks.' +transaction['stock']: {
                            'stock': transaction['stock'], 
                            'amount': transaction['amount'], 
                            'price': [
                                {
                                    str(transaction['amount']): transaction['price']
                                }
                            ]
                        },
                        'pending_buy': None
                    },
                    '$push': {
                        'transactions': transaction
                    },
                    '$inc': {
                        'balance': -transaction['amount'] * transaction['price']
                    }
                }, func = db.user.update_one, eventLog = {'type': 'accountTransaction', 'username': str(id), 'timestamp': int(time.time()), 'action': 'BUY_SHARES', 'stock': transaction['stock'], 'amount': transaction['amount'], 'price': transaction['price'], 'cryptographicKey': transaction['cryptographicKey'], 'transactionId': transactionId})
            
            
            

            return True
    raise Exception('No pending transaction')

def sellStock(id, amount, quote, transactionId):
    id = ObjectId(id)
    user = getUser(id)
    price = quote['price']
    stock = quote['ticker']
    timestamp = quote['timestamp']
    cryptographicKey = quote['cryptographicKey']

    # check if the user has enough of the stock to sell
    if(stock in user['stocks'].keys() and user['stocks'][stock]['amount'] >= amount):
       
        # set the transaction to the user's pending transaction
        dbCallWrapper(
            {'_id': id}, {
                '$set': {
                    'pending_sell': {
                        'stock': stock, 
                        'amount': amount,
                        'price': price, 
                        'timestamp': timestamp, 
                        'cryptographicKey': cryptographicKey
                    }
                }
            }, 
            func = db.user.update_one,
            eventLog = {'type': 'debugEvent', 'username': str(id), 'timestamp': int(time.time()), 'action': 'SELL', 'stock': stock, 'amount': amount, 'price': price, 'cryptographicKey': cryptographicKey, 'transactionId': transactionId}
        )
        return True
    raise Exception('Insufficient stock')

def commitSell(id, transactionId):
    id = ObjectId(id)
    user = getUser(id)
    transaction = user['pending_sell']
    if(transaction):
        if(time.time() - transaction['timestamp'] > 60):
            # clear the pending transaction
            dbCallWrapper({'_id': id}, {'$set': {'pending_sell': None}}, func = db.user.update_one)
            raise Exception('Quote expired')
        else:
            # sell the stock
            totalAmount = user['stocks'][transaction['stock']]['amount']

            if(totalAmount == transaction['amount']):
                dbCallWrapper(
                    {'_id': id}, {
                        '$inc': {
                            'stocks.' + transaction['stock'] + '.amount': -transaction['amount'],
                            'balance': transaction['amount'] * transaction['price']
                        },
                        '$push':{
                            'transactions': transaction
                        },
                        '$set': {
                            'pending_sell': None,
                            'stocks.' + transaction['stock']: None
                        }
                    }, 
                    func = db.user.update_one,
                    eventLog = {'type': 'accountTransaction', 'username': str(id), 'timestamp': int(time.time()), 'action': 'SELL_SHARES', 'stock': transaction['stock'], 'amount': transaction['amount'], 'price': transaction['price'], 'cryptographicKey': transaction['cryptographicKey'], 'transactionId': transactionId}
                )
            else:

                dbCallWrapper({'_id': id}, {
                    '$inc': {
                        'stocks.' + transaction['stock'] + '.amount': -transaction['amount'],
                        'balance': transaction['amount'] * transaction['price']
                    },
                    '$push':{
                        'transactions': transaction,
                        'stocks.' + transaction['stock'] + '.price': {
                            -transaction['amount']: transaction['price']
                        }
                    },
                    '$set': {
                        'pending_sell': None
                    }
                }, func = db.user.update_one, eventLog = {'type': 'accountTransaction', 'username': str(id), 'timestamp': int(time.time()), 'action': 'SELL_SHARES', 'stock': transaction['stock'], 'amount': transaction['amount'], 'price': transaction['price'], 'cryptographicKey': transaction['cryptographicKey'], 'transactionId': transactionId})

            return True
    raise Exception('No pending transaction')

def cancelSell(id, transactionId):
    id = ObjectId(id)
    # clear the pending transaction
    if (getUser(id)['pending_sell']):
        dbCallWrapper({'_id': id}, {'$set': {'pending_sell': None}}, func = db.user.update_one, eventLog = {'type': 'debugEvent', 'username': str(id), 'timestamp': int(time.time()), 'action': 'CANCEL_SELL', 'transactionId': transactionId})
        return True
    raise Exception('No pending buy')

def cancelBuy(id, transactionId):
    id = ObjectId(id)
    # clear the pending transaction
    if (getUser(id)['pending_buy']):
        dbCallWrapper({'_id': id}, {'$set': {'pending_buy': None}}, func = db.user.update_one, eventLog = {'type': 'debugEvent', 'username': str(id), 'timestamp': int(time.time()), 'action': 'CANCEL_BUY', 'transactionId': transactionId})
        return True
    raise Exception('No pending buy')


def setBuyAmount(id, stock, amount, transactionId):
    id = ObjectId(id)
    
    return dbCallWrapper({'_id': id}, {
        '$set': {
            'pending_trigger': {
                'stock': stock,
                'amount': amount,
                'type': 'buy'
            }
        }
    }, func = db.user.update_one, 
    eventLog = {'type': 'debugEvent', 'username': str(id), 'timestamp': int(time.time()), 'action': 'SET_BUY_AMOUNT', 'stock': stock, 'amount': amount, 'transactionId': transactionId})
    

def setSellAmount(id, stock, amount, transactionId):
    id = ObjectId(id)

    return dbCallWrapper({'_id': id}, {
        '$set': {
            'pending_trigger': {
                'stock': stock,
                'amount': amount,
                'type': 'sell'
                }
        }
    }, func = db.user.update_one, eventLog={'type': 'debugEvent', 'username': str(id), 'timestamp': int(time.time()), 'action': 'SET_BUY_AMOUNT', 'stock': stock, 'amount': amount, 'transactionId': transactionId})

def setBuyTrigger(id, stock, price, transactionId):
    id = ObjectId(id)
    
    if(getUser(id)['pending_trigger']['stock'] == stock and getUser(id)['pending_trigger']['type'] == 'buy'):
        return dbCallWrapper({'_id': id}, {
            '$set': {
                'pending_trigger': None,
                'triggers'+'.'+stock: {
                    'amount': getUser(id)['pending_trigger']['amount'],
                    'price': price,
                    'userid': id
                    
                }
            }
        }, func = db.user.update_one,
        eventLog = {'type': 'debugEvent', 'username': str(id), 'timestamp': int(time.time()), 'action': 'SET_BUY_TRIGGER', 'stock': stock, 'price': price, 'transactionId': transactionId})
        
    raise Exception('No pending trigger')

def setSellTrigger(id, stock, price, transactionId):
    id = ObjectId(id)

    if(getUser(id)['pending_trigger']['stock'] == stock and getUser(id)['pending_trigger']['type'] == 'sell'):
        return dbCallWrapper({'_id': id}, {
            '$set': {
                'pending_trigger': None,
                'sell_triggers': {
                    stock: {
                        'amount': getUser(id)['pending_trigger']['amount'],
                        'price': price,
                        'userid': id
                    }
                }
            }
        }, func = db.user.update_one, eventLog = {'type': 'debugEvent', 'username': str(id), 'timestamp': int(time.time()), 'action': 'SET_BUY_TRIGGER', 'stock': stock, 'price': price, 'transactionId': transactionId})
    raise Exception('No pending trigger')
def cancelSellTrigger(id, stock, transactionId):
    id = ObjectId(id)
    user = getUser(id)
    if(user['sell_triggers'][stock] and user['triggers'][stock]['type'] == 'sell'):
        return dbCallWrapper({'_id': id}, {
            '$set': {
                'triggers.' + stock: None
            }
        }, func = db.user.update_one, eventLog={'type': 'debugEvent', 'username': str(id), 'timestamp': int(time.time()), 'action': 'CANCEL_SELL_TRIGGER', 'stock': stock, 'transactionId': transactionId})
    raise Exception('No active sell trigger on specified stock')

def cancelBuyTrigger(id, stock, transactionId):
    id = ObjectId(id)
    user = getUser(id)
    if(user['buy_triggers'][stock] and user['buy_triggers'][stock]['type'] == 'buy'):
        return dbCallWrapper({'_id': id}, {
            '$set': {
                'triggers.' + stock: None
            }
        }, func = db.user.update_one, eventLog = {'type': 'debugEvent', 'username': str(id), 'timestamp': int(time.time()), 'action': 'CANCEL_SELL_TRIGGER', 'stock': stock, 'transactionId': transactionId})

def getTriggers():

    return dbCallWrapper({}, {'buy_triggers': 1, 'sell_triggers': 1}, func = db.user.find, eventLog = False)

def dumplogXML(id = None):
    if(id):
        id = id
        docs = dbCallWrapper({'username': id}, {}, func = db.log.find, eventLog = False)
    else:
        docs = dbCallWrapper({}, {}, func = db.log.find, eventLog = False)
    print(docs)
    new_docs = '<?xml version="1.0" encoding="US-ASCII"?>\n\t<log>'
    for doc in docs:
        new_docs += '\t<'+doc['type']+'>\n'
        if 'transactionId' in doc.keys():
            new_docs += '\t\t<transactionId>'+str(doc['transactionId'])+'</transactionId>\n'
        else:
            new_docs += '\t\t<transactionId>'+str(doc['_id'])+'</transactionId>\n'
        for key in doc:
            if key != 'type' and key != '_id' and key != 'transactionId':
                new_docs += '\t\t<'+key+'>'+str(doc[key])+'</'+key+'>\n'
        new_docs += '\t</'+doc['type']+'>\n'
    new_docs += '</log>'
    return new_docs
            