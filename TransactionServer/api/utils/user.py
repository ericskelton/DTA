
from api.utils.db import getDb
import time
from api.utils.quoteServer import getQuote
from hashlib import sha256

db, client = getDb('dta')

def getBalance(id):
    return db.user.find_one({'_id': id}, {'balance': 1})

def addBalance(id, amount):
    return db.user.update_one({'_id': id}, {'$inc': {'balance': amount}})

def subBalance(id, amount):
    return db.user.update_one({'_id': id}, {'$inc': {'balance': -amount}})

def getTransactions(id):
    return db.user.find_one({'_id': id}, {'transactions': 1})

def getAllTransactions():
    return db.user.find({}, {'transactions': 1})

def getUser(id):
    return db.user.find_one({'_id': id})

def addTransaction(id, transaction):
    return db.user.update_one({'_id': id}, {'$push': {'transactions': transaction}})

def addStock(id, stock, amount):
    return db.user.update_one({'_id': id}, {'$push': {'stocks': {'stock': stock, 'amount': amount}}})

def createUser(name, email, password):
    # email must be unique
    if(db.user.find_one({'email': email})):
        return False

    return db.user.insert_one({
        'name': name,
        'email': email,
        'password': sha256(password.encode('utf-8')).hexdigest(),
        'balance': 0.00, 
        'transactions': [], 
        'stocks': [],
        'pending_transactions': [],
        'transaction_triggers': []
        })

def login(email, password):
    user = db.user.find_one({'email': email, 'password': sha256(password.encode('utf-8')).hexdigest()})

    if(user):
        # TODO: generate token, save against user somehow, return token
        return user
    else:
        return False

# sets the pending transaction to the pending transaction field on the user
# fails if the user does not have enough balance
def buyStock(id, stock, amount, price, timestamp, cryptographicKey):
    user = getUser(id)
    # check if the user has enough balance to buy
    if(user['balance'] >= amount * price):

        # set pending transaction
        db.user.update_one({'_id': id}, {
            '$set': {
                'pending_buy' : {
                    'stock': stock, 
                    'amount': amount, 
                    'price': price, 
                    'timestamp': timestamp, 
                    'cryptographicKey': cryptographicKey
                }
            }
        })
        return True
    return False
    
# gets the pending transactions for a user
def getPendingTransaction(id):
    return db.user.find_one({'_id': id}, {'': 1})
# removes the pending transaction from the transactions list
# adds the transaction to the transactions list
# if the any quote is over 2 minutes old, we fail and refresh the quote for each expired quote
def commitBuy(id):
    user = getUser(id)
    transaction = user['pending_transaction']
    if(transaction):
        if(time.time() - transaction['timestamp'] > 60):
            # clear the pending transaction
            db.user.update_one({'_id': id}, {'$set': {'pending_transaction': None}})
            return False
        else:
            # buy the stock
            if(transaction['stock'] in user['stocks'].keys()):
                db.user.update_one({'_id': id}, {
                    '$inc': {
                        'stocks.' + transaction['stock'] + '.amount': transaction['amount'],
                        'balance': -transaction['amount'] * transaction['price']
                    }, 
                    '$push':{
                        'stocks.' + transaction['stock'] + 'price': {
                            transaction['amount']: transaction['price']
                        },
                        'transactions': transaction
                    },
                    '$set': {'pending_transaction': None}
                })
                
            else:
                db.user.update_one({'_id': id}, {
                    '$set': {
                        'stocks.' +transaction['stock']: {
                            'stock': transaction['stock'], 
                            'amount': transaction['amount'], 
                            'price': [
                                {
                                    transaction['amount']: transaction['price']
                                }
                            ]
                        },
                        'pending_transaction': None
                    },
                    '$push': {
                        'transactions': transaction
                    },
                    '$inc': {
                        'balance': -transaction['amount'] * transaction['price']
                    }
                })
            
            
            

            return True

def sellStock(id, stock, amount, price, timestamp, cryptographicKey):
    user = getUser(id)
    # check if the user has enough of the stock to sell
    if(stock in user['stocks'].keys() and user['stocks'][stock]['amount'] >= amount):
        # check if the user has a pending transaction for this stock
        if user.pending_sell:
            return False
        else:
            # set the transaction to the user's pending transaction
            db.user.update_one({'_id': id}, {
                '$set': {
                    'pending_sell': {
                        'stock': stock, 
                        'amount': amount,
                        'price': price, 
                        'timestamp': timestamp, 
                        'cryptographicKey': cryptographicKey
                    }
                }
            })
            return True
    return False

def commitSell(id):
    user = getUser(id)
    transaction = user['pending_sell']
    if(transaction):
        if(time.time() - transaction['timestamp'] > 60):
            # clear the pending transaction
            db.user.update_one({'_id': id}, {'$set': {'pending_sell': None}})
            return False
        else:
            # sell the stock
            totalAmount = user['stocks'][transaction['stock']]['amount']

            if(totalAmount == transaction['amount']):
                db.user.update_one({'_id': id}, {
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
                    }})
            else:
                db.user.update_one({'_id': id}, {
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
                })

            return True
    return False

def cancelSell(id):
    # clear the pending transaction
    db.user.update_one({'_id': id}, {'$set': {'pending_sell': None}})
    return True

def cancelBuy(id):
    # clear the pending transaction
    db.user.update_one({'_id': id}, {'$set': {'pending_buy': None}})
    return True

def dumplog(id):
    transactions = db.user.find_one({'_id': id}, {'transactions': 1})
    return transactions['transactions']

