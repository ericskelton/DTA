
from api.utils.db import getDb
import time
from api.utils.quoteServer import getQuote
from hashlib import sha256
from bson.objectid import ObjectId
from api.utils.db import dbCallWrapper
import xml.dom

db, client = getDb()

def getBalance(username):
    return dbCallWrapper({'username': username}, {'balance': 1}, func = db.user.find_one, eventLog = False)

def addBalance(username, amount, transactionId):
    print('amount', amount)
    return dbCallWrapper({"username": username}, {'$inc': {'balance': float(amount)}}, func = db.user.update_one, eventLog = {'type': 'debugEvent', 'username': str(username), 'timestamp': int(time.time()), 'action': 'ADD_BALANCE', 'amount': amount, 'transactionId': transactionId})


def subBalance(username, amount):
    return dbCallWrapper({'username': username}, {'$inc': {'balance': -float(amount)}}, func = db.user.update_one, eventLog = False) 

def getTransactions(username):
    return dbCallWrapper({'username': username}, {'transactions': 1}, func = db.user.find_one, eventLog = False)

def getAllTransactions():
    return dbCallWrapper({}, {'transactions': 1}, func = db.user.find, eventLog = False)

def getUser(username):
    return dbCallWrapper({"username": username}, func = db.user.find_one, eventLog = False)

def addTransaction(username, transaction):
    return dbCallWrapper({'username': username}, {'$push': {'transactions': transaction}}, func = db.user.update_one)


def createUser(name, username, password):
    # username must be unique
    if(db.user.find_one({'username': username})): # don't need to wrap this 
        raise Exception('username already in use')

    return dbCallWrapper({
        'name': name,
        'username': username,
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

def login(username, password):
    user = dbCallWrapper({'username': username, 'password': sha256(password.encode('utf-8')).hexdigest()}, func = db.user.find_one)

    if(user):
        # TODO: generate token, return token
        return user
    else:
        return False

# sets the pending transaction to the pending transaction field on the user
# fails if the user does not have enough balance
def buyStock(username, amount, quote, transactionId):
    price = quote['price']
    stock = quote['ticker']
    timestamp = quote['timestamp']
    cryptographicKey = quote['cryptographicKey']
    user = getUser(username)
    amount = float(amount)
    # check if the user has enough balance to buy
    if(user['balance'] >= amount * price):

        # set pending transaction
        dbCallWrapper({'username': username}, {
            '$set': {
                'pending_buy' : {
                    'stock': stock, 
                    'amount': amount, 
                    'price': price, 
                    'timestamp': timestamp, 
                    'cryptographicKey': cryptographicKey
                }
            }
        }, func = db.user.update_one, eventLog = {'type': 'debugEvent', 'username': str(username), 'timestamp': timestamp, 'action': 'BUY', 'stock': stock, 'amount': amount, 'price': price, 'cryptographicKey': cryptographicKey, 'transactionId': transactionId})
        return {
            'stock': stock,
            'amount': amount,
            'price': price,
            'timestamp': timestamp,
        }
    raise Exception('Insufficient balance, stock is {}, price is {}, amount is {}, balance is {}, total price is {}'.format(stock, str(price), str(amount), str(user['balance']), str(amount * price)))

# removes the pending buy
# adds the transaction to the transactions list
# if the any quote is over 1 minute old, we fail 
def commitBuy(username, transactionId):
    user = getUser(username)
    transaction = user['pending_buy']
    if(transaction):
        if(int(time.time() * 1000) - float(transaction['timestamp']) > 60000):
            # clear the pending transaction
            db.user.update_one({'username': username}, {'$set': {'pending_buy': None}})
            raise Exception('Quote expired')
        else:
            # buy the stock
            if(transaction['stock'] in user['stocks']):
                dbCallWrapper( {'username': username}, {
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
                }, func = db.user.update_one, eventLog = {'type': 'accountTransaction', 'username': str(username), 'timestamp': int(time.time()), 'action': 'BUY_SHARES', 'stock': transaction['stock'], 'amount': transaction['amount'], 'price': transaction['price'], 'cryptographicKey': transaction['cryptographicKey'], 'transactionId': transactionId})
                
            else:
                dbCallWrapper( {'username': username}, {
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
                }, func = db.user.update_one, eventLog = {'type': 'accountTransaction', 'username': str(username), 'timestamp': int(time.time()), 'action': 'BUY_SHARES', 'stock': transaction['stock'], 'amount': transaction['amount'], 'price': transaction['price'], 'cryptographicKey': transaction['cryptographicKey'], 'transactionId': transactionId})
            
            
            

            return True
    raise Exception('No pending transaction')

def sellStock(username, amount, quote, transactionId):
    user = getUser(username)
    price = quote['price']
    stock = quote['ticker']
    timestamp = quote['timestamp']
    cryptographicKey = quote['cryptographicKey']
    if(stock not in user['stocks'].keys()):
        raise Exception('Stock not owned')
    # check if the user has enough of the stock to sell
    if(stock in user['stocks'].keys() and user['stocks'][stock]['amount'] >= float(amount)):
       
        # set the transaction to the user's pending transaction
        dbCallWrapper(
            {'username': username}, {
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
            eventLog = {'type': 'debugEvent', 'username': str(username), 'timestamp': timestamp, 'action': 'SELL', 'stock': stock, 'amount': amount, 'price': price, 'cryptographicKey': cryptographicKey, 'transactionId': transactionId}
        )
        return True
    raise Exception('Insufficient stock')

def commitSell(username, transactionId):
    user = getUser(username)
    transaction = user['pending_sell']
    if(transaction):
        if(time.time() - float(transaction['timestamp']) > 60):
            # clear the pending transaction
            dbCallWrapper({'username': username}, {'$set': {'pending_sell': None}}, func = db.user.update_one)
            raise Exception('Quote expired')
        else:
            # sell the stock
            totalAmount = user['stocks'][transaction['stock']]['amount']

            if(totalAmount == transaction['amount']):
                dbCallWrapper(
                    {'username': username}, {
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
                    eventLog = {'type': 'accountTransaction', 'username': str(username), 'timestamp': int(time.time()), 'action': 'SELL_SHARES', 'stock': transaction['stock'], 'amount': transaction['amount'], 'price': transaction['price'], 'cryptographicKey': transaction['cryptographicKey'], 'transactionId': transactionId}
                )
            else:

                dbCallWrapper({'username': username}, {
                    '$inc': {
                        'stocks.' + transaction['stock'] + '.amount': -transaction['amount'],
                        'balance': transaction['amount'] * transaction['price']
                    },
                    '$push':{
                        'transactions': transaction,
                        'stocks.' + transaction['stock'] + '.price': {
                            '-' + str(transaction['amount']): transaction['price']
                        }
                    },
                    '$set': {
                        'pending_sell': None
                    }
                }, func = db.user.update_one, eventLog = {'type': 'accountTransaction', 'username': str(username), 'timestamp': int(time.time()), 'action': 'SELL_SHARES', 'stock': transaction['stock'], 'amount': transaction['amount'], 'price': transaction['price'], 'cryptographicKey': transaction['cryptographicKey'], 'transactionId': transactionId})

            return True
    raise Exception('No pending transaction')

def cancelSell(username, transactionId):
    # clear the pending transaction
    if (getUser(username)['pending_sell']):
        dbCallWrapper({'username': username}, {'$set': {'pending_sell': None}}, func = db.user.update_one, eventLog = {'type': 'debugEvent', 'username': str(username), 'timestamp': int(time.time()), 'action': 'CANCEL_SELL', 'transactionId': transactionId})
        return True
    raise Exception('No pending sell')

def cancelBuy(username, transactionId):
    # clear the pending transaction
    if (getUser(username)['pending_buy']):
        dbCallWrapper({'username': username}, {'$set': {'pending_buy': None}}, func = db.user.update_one, eventLog = {'type': 'debugEvent', 'username': str(username), 'timestamp': int(time.time()), 'action': 'CANCEL_BUY', 'transactionId': transactionId})
        return True
    raise Exception('No pending buy')


def setBuyAmount(username, stock, amount, transactionId):
    
    return dbCallWrapper({'username': username}, {
        '$set': {
            'pending_trigger': {
                'stock': stock,
                'amount': amount,
                'type': 'buy'
            }
        }
    }, func = db.user.update_one, 
    eventLog = {'type': 'debugEvent', 'username': str(username), 'timestamp': int(time.time()), 'action': 'SET_BUY_AMOUNT', 'stock': stock, 'amount': amount, 'transactionId': transactionId})
    

def setSellAmount(username, stock, amount, transactionId):

    return dbCallWrapper({'username': username}, {
        '$set': {
            'pending_trigger': {
                'stock': stock,
                'amount': amount,
                'type': 'sell'
                }
        }
    }, func = db.user.update_one, eventLog={'type': 'debugEvent', 'username': str(username), 'timestamp': int(time.time()), 'action': 'SET_BUY_AMOUNT', 'stock': stock, 'amount': amount, 'transactionId': transactionId})

def setBuyTrigger(username, stock, price, transactionId):
    user = getUser(username)
    if(user['pending_trigger']['stock'] == stock and user['pending_trigger']['type'] == 'buy'):
        return dbCallWrapper({'username': username}, {
            '$set': {
                'pending_trigger': None,
                'buy_triggers'+'.'+stock: {
                    'amount': user['pending_trigger']['amount'],
                    'price': price,
                    'userid': username,
                    'type': 'buy'
                    
                }
            }
        }, func = db.user.update_one,
        eventLog = {'type': 'debugEvent', 'username': str(username), 'timestamp': int(time.time()), 'action': 'SET_BUY_TRIGGER', 'stock': stock, 'price': price, 'transactionId': transactionId})
        
    raise Exception('No pending trigger')

def setSellTrigger(username, stock, price, transactionId):
    user = getUser(username)

    if(user['pending_trigger']['stock'] == stock and user['pending_trigger']['type'] == 'sell'):
        return dbCallWrapper({'username': username}, {
            '$set': {
                'pending_trigger': None,
                'sell_triggers': {
                    stock: {
                        'amount': user['pending_trigger']['amount'],
                        'price': price,
                        'userid': username,
                        'type': 'sell'
                    }
                }
            }
        }, func = db.user.update_one, eventLog = {'type': 'debugEvent', 'username': str(username), 'timestamp': int(time.time()), 'action': 'SET_BUY_TRIGGER', 'stock': stock, 'price': price, 'transactionId': transactionId})
    raise Exception('No pending trigger')
def cancelSellTrigger(username, stock, transactionId):
    user = getUser(username)
    if(user['sell_triggers'][stock] and user['sell_triggers'][stock]['type'] == 'sell'):
        return dbCallWrapper({'username': username}, {
            '$set': {
                'sell_triggers.' + stock: None
            }
        }, func = db.user.update_one, eventLog={'type': 'debugEvent', 'username': str(username), 'timestamp': int(time.time()), 'action': 'CANCEL_SELL_TRIGGER', 'stock': stock, 'transactionId': transactionId})
    raise Exception('No active sell trigger on specified stock')

def cancelBuyTrigger(username, stock, transactionId):
    user = getUser(username)
    if(user['buy_triggers'][stock] and user['buy_triggers'][stock]['type'] == 'buy'):
        return dbCallWrapper({'username': username}, {
            '$set': {
                'buy_triggers.' + stock: None
            }
        }, func = db.user.update_one, eventLog = {'type': 'debugEvent', 'username': str(username), 'timestamp': int(time.time()), 'action': 'CANCEL_SELL_TRIGGER', 'stock': stock, 'transactionId': transactionId})

def getTriggers():

    return dbCallWrapper({}, {'buy_triggers': 1, 'sell_triggers': 1}, func = db.user.find, eventLog = False)


# TODO rewrite this
def dumplogXML(username = None):
    if(username):
        docs = dbCallWrapper({'username': username}, {}, func = db.log.find, eventLog = False)
    else:
        docs = dbCallWrapper({}, {}, func = db.log.find, eventLog = False)
    new_docs = '<?xml version="1.0"?>\n\t<log>'
    transactionids = []
    for doc in docs:
        new_docs += '\t<'+doc['type']+'>\n'
        
        
        # go through the keys and add them to the xml
        for key in doc:
            if key == 'ticker':
                new_docs += '\t\t<stockSymbol>'+doc[key]+'</stockSymbol>\n'
            elif key == 'amount':
                new_docs += '\t\t<funds>'+str(doc[key])+'</funds>\n'
            elif key == 'command':
                new_docs += '\t\t<command>'+doc[key].upper()+'</command>\n'
            elif key == 'userid':
                new_docs += '\t\t<username>'+doc[key]+'</username>\n'
            elif key == 'transactionNum':
                new_docs += '\t\t<transactionNum>'+str(doc[key])+'</transactionNum>\n'
            elif key == 'timestamp':
                if int(doc[key]) * 1000 > 10000000000000:
                    value = int(doc[key])
                else: 
                    value = int(doc[key]) * 1000
                new_docs += '\t\t<timestamp>'+str(value)+'</timestamp>\n'
            elif key != 'type' and key != '_id' and key != 'transactionId':
                new_docs += '\t\t<'+key+'>'+str(doc[key])+'</'+key+'>\n'
        new_docs += '\t</'+doc['type']+'>\n'
    new_docs += '</log>'
    return new_docs

def displayUserSummary(username):
    user = getUser(username)
    return {'username': user['username'], 'balance': user['balance'], 'stocks': user['stocks'], 'triggers': user['buy_triggers'].update(user['sell_triggers']), 'transactions': user['transactions']}