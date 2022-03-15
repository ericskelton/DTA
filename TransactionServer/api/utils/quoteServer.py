import socket
from api.utils.db import *
import time
import random
db, client = getDb()
def getQuote(ticker, user, transactionId):
    #try:
    #    HOST = '192.168.4.2'
    #    PORT = 4444
    #    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    #        try:
    #            sock.connect((HOST, PORT))
    #        except socket.error as err:
    #            print('Error connecting to server: {}'.format(err))
#
    #        sock.sendall(ticker.encode()+ b' ' + userid.encode() + b'\n')
    #        data = sock.recv(1024)
    #    decodedData = data.decode().split(',')
#
    #    logJsonObject({
    #        'ticker': ticker,
    #        'price': decodedData[0],
    #        'username': decodedData[1],
    #        'timestamp': decodedData[2],
    #        'cryptographicKey': decodedData[3],
    #        'type': 'quoteServer',
    #        'transactionId': transactionId
    #    })
#
    #    return {
    #        'ticker': ticker,
    #        'price': decodedData[0],
    #        'username': decodedData[1],
    #        'timestamp': decodedData[2],
    #        'cryptographicKey': decodedData[3]
    #    }
    #except Exception as e:
        randomFloat = (random.uniform(0, 1) * 250) + 50
        randomFloat = float(str(randomFloat).split('.')[0] +'.' + str(randomFloat).split('.')[1][:2])
        # generate random key
        from key_generator.key_generator import generate
        current_time = int(time.time() * 1000)
        key = generate(seed = randomFloat//1).get_key()
        quote = dbCallWrapper({"type": "quoteServer", "stockSymbol": ticker, 'timestamp': {"$gt": current_time - 60000}}, func = db.log.find_one)
        if quote:
            key = quote['cryptokey']
            quote = quote['price']
        
        randomFloat = quote if quote else randomFloat
        fetchType = 'quoteServer' if not quote else 'quote_cache'
        if fetchType == 'quoteServer':

            logJsonObject({
                # QUOTE SERVER LOG 
                'stockSymbol': ticker,
                'price': randomFloat,
                'username': user['username'],
                'quoteServerTime': random.randint(1,5),
                'timestamp': current_time,
                'cryptokey': key,
                'server': 'transactionserver',
                'type': fetchType,
            })
        else:
            logJsonObject({
                # SYSTEM EVENT LOG FOR CACHE
                'username': user['username'],
                'timestamp': current_time,
                'server': 'transactionserver',
                'type': 'debugEvent',
                'debugMessage': 'Quote Server Cache Hit for ' + ticker
            })
        return {
            'ticker': ticker,
            'price': randomFloat,
            'username': user['username'],
            'timestamp': current_time,
            'cryptographicKey': key,
        }





